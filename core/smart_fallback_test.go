package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"

	"github.com/metacubex/mihomo/config"
	yaml "go.yaml.in/yaml/v3"
)

func smartProfile(t *testing.T) string {
	t.Helper()
	data, err := os.ReadFile("../examples/smart-fallback.yaml")
	if err != nil {
		t.Fatal(err)
	}
	return strings.Replace(string(data), "enabled: false", "enabled: true", 1)
}

func TestSmartFallbackRuntimeRoundTrip(t *testing.T) {
	for _, scripted := range []bool{false, true} {
		t.Run(map[bool]string{false: "imported-yaml", true: "script-override"}[scripted], func(t *testing.T) {
			source := smartProfile(t)
			var original map[string]any
			if err := yaml.Unmarshal([]byte(source), &original); err != nil {
				t.Fatal(err)
			}
			path := filepath.Join(t.TempDir(), "profile.yaml")
			if scripted {
				data, err := json.Marshal(original)
				if err != nil {
					t.Fatal(err)
				}
				source = string(data)
			}
			if err := os.WriteFile(path, []byte(source), 0600); err != nil {
				t.Fatal(err)
			}
			params := &SetupParams{ProfilePath: path, OverrideTestUrl: true, TestURL: "https://example.invalid/global-test", Patch: &PatchParams{General: []byte(`{"mixed-port":17891}`), HealthCheckTimeout: 5000}}
			if scripted {
				params.ScriptedConfig = path
				params.ProfilePath = ""
			}
			out, err := handleGetRuntimeConfig(params)
			if err != nil {
				t.Fatal(err)
			}
			var saved map[string]any
			if err := yaml.Unmarshal([]byte(out), &saved); err != nil {
				t.Fatal(err)
			}
			group := saved["proxy-groups"].([]any)[0].(map[string]any)
			want := original["proxy-groups"].([]any)[0].(map[string]any)
			if !reflect.DeepEqual(group["smart-fallback"], want["smart-fallback"]) {
				t.Fatalf("enhanced fields changed: %#v", group)
			}
			if saved["mixed-port"] != 17891 {
				t.Fatalf("patch not applied: %#v", saved)
			}
			if _, err := config.Parse([]byte(out)); err != nil {
				t.Fatalf("saved config rejected: %v", err)
			}
			if scripted {
				if err := os.WriteFile(path, []byte(source), 0600); err != nil {
					t.Fatal(err)
				}
			}
			prepared, err := prepareSetup(params)
			if err != nil {
				t.Fatal(err)
			}
			if got := prepared.rawCfg.ProxyGroup[0]["url"]; got != want["url"] {
				t.Fatalf("global test URL broke enhanced health task: %v", got)
			}
			if got, _ := os.ReadFile(path); !scripted && string(got) != source {
				t.Fatal("source profile mutated")
			}
		})
	}
}

func TestSmartFallbackValidationErrorsReachClient(t *testing.T) {
	for _, invalid := range []string{"failure-threshold: 0", "failure-threshold: 1.5", "failure-threshold: bogus"} {
		t.Run(invalid, func(t *testing.T) {
			source := strings.Replace(smartProfile(t), "failure-threshold: 3", invalid, 1)
			if got := handleValidateConfig(&ValidateConfigParams{Data: source}); !strings.Contains(got, "smart-fallback") {
				t.Fatalf("lost core validation error: %q", got)
			}
			path := filepath.Join(t.TempDir(), "invalid.yaml")
			if err := os.WriteFile(path, []byte(source), 0600); err != nil {
				t.Fatal(err)
			}
			params := &SetupParams{ProfilePath: path, Patch: &PatchParams{General: []byte(`{"mixed-port":17891}`), HealthCheckTimeout: 5000}}
			out, err := handleGetRuntimeConfig(params)
			if err != nil {
				t.Fatal(err)
			}
			if got := handleValidateConfig(&ValidateConfigParams{Data: out}); !strings.Contains(got, "smart-fallback") {
				t.Fatalf("runtime config hid invalid parameter: %q", got)
			}
			if _, err := prepareSetup(params); err == nil || !strings.Contains(err.Error(), "smart-fallback") {
				t.Fatalf("startup hid validation error: %v", err)
			}
		})
	}
}

func TestOrdinaryFallbackRemainsDefault(t *testing.T) {
	source := strings.Replace(smartProfile(t), "enabled: true", "enabled: false", 1)
	if got := handleValidateConfig(&ValidateConfigParams{Data: source}); got != "" {
		t.Fatal(got)
	}
	source = strings.Replace(source, "    smart-fallback:\n      enabled: false\n      window: 600\n      failure-threshold: 3\n      cooldown: [1800, 3600, 7200]\n      recover-success: 3\n      reset-after: 3600\n", "", 1)
	if got := handleValidateConfig(&ValidateConfigParams{Data: source}); got != "" {
		t.Fatal(got)
	}
}
