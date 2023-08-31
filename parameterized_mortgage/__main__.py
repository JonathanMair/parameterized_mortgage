from parameterized_mortgage.dashboard import panel_dashboard
import sys



if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "demo":
        panel_dashboard.demo()
