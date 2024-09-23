# copilot-code-review

This is a tool that combines LLM model's capability with GitHub action in CI Pipeline to improve development efficiency and quality.

## How To Use

### Set Up Azure AI Service 

In the Settings of your repo, under `Actions` of `Secrets and variables` tab, please add `APIKEY` and `ENDPOINT` into repository secrets and their value can be get from your registered Azure AI Service.

### Add action into workflow

In your workflow file, please include the code snippet below into it
```yaml
  - name: Copilot PR Review
    uses: AllyW/copilot-pr-review@<your target version like v0.1.33>
    with:
      APIKEY: ${{ secrets.APIKEY }}
      ENDPOINT: ${{ secrets.ENDPOINT }}
      AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      PR_EVENT: ${{ toJSON(github.event) }}
      code_suggest: True
      pr_summary: True
      pr_reset: True
```

## Usages

For now, except the necessary auth keys of ai service, there are four parameters developers can apply on demand.
1. `code_suggest`: Whether review pr code change by line of patch, default: `False`
2. `pr_summary`: Whether draw a conclusion from whole pr diff, default: `True`
3. `pr_reset`: Whether clean last round pr reviews, default: `True`
4. `review_filter`: Whether filter review result by evaluation process

