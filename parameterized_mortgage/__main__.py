from parameterized_mortgage.dashboard import panel_dashboard
import panel as pn
import sys

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "demo":
        template = panel_dashboard.get_dashboard_demo()
        pn.serve(template, threaded=True)
