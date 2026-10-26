Google Colab run (Linux) of mutmut for the AI-only, manual-only, combined and AI+targeted suites. WSL was not available on the Windows PC, so mutmut ran in Colab.
Results: AI-only killed 38 / survived 1 (app.cli.x_main__mutmut_13); manual-only, combined and AI+targeted killed 39 / survived 0.
The red CalledProcessError at the bottom of the second screenshot is only the final `grep survived` returning exit code 1 because there were no survivors.
