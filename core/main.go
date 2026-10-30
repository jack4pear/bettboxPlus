//go:build !cgo

package main

import (
	"fmt"
	"github.com/metacubex/mihomo/constant"
	"os"
)

func main() {
	args := os.Args
	if len(args) == 2 && args[1] == "--version" {
		fmt.Println(constant.Version)
		return
	}
	if len(args) <= 1 {
		fmt.Println("Arguments error")
		os.Exit(1)
	}
	startServer(args[1])
}
