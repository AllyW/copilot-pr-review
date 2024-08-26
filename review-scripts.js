import { OpenAIClient, AzureKeyCredential } from "@azure/openai";
import { Octokit } from "@octokit/rest";

const repository = process.env.REPO;
const token = process.env.TOKEN;
const event = process.env.EVENT;
const endpoint = process.env.ENDPOINT;
const apiKey = process.env.APIKEY;
const model = "gpt-4o";
const MAX_PATCH_COUNT = 500;

const client = new OpenAIClient(endpoint, new AzureKeyCredential(apiKey));
// send msg to chatgpt
async function chat(patch) {
  const { choices } = await client.getChatCompletions(model, [
    {
      role: "user",
      content: `Below is the diff info of from a github pull requests, please make a simple code review, and find the places that can be refined, in a simple and concise way:
        "${patch}"
      `,
    },
  ]);
  return choices[0]?.message?.content;
}

// get pr information
const [owner, repo] = repository.split("/");
const { pull_request, number } = JSON.parse(event);

const octokit = new Octokit({
  auth: token,
});

const { data } = await octokit.rest.repos.compareCommits({
  owner,
  repo,
  base: pull_request.base.sha,
  head: pull_request.head.sha,
});

const { files: changedFiles, commits } = data;

for (let i = 0; i < changedFiles.length; i++) {
  const file = changedFiles[i];
  const patch = file.patch || "";

  if (file.status !== "modified" && file.status !== "added") {
    continue;
  }

  if (!patch || patch.length > MAX_PATCH_COUNT) {
    continue;
  }

  const res = await chat(patch);

  if (!!res) {
    await octokit.pulls.createReviewComment({
      owner,
      repo,
      pull_number: number,
      commit_id: commits[commits.length - 1].sha,
      path: file.filename,
      body: res,
      position: patch.split("\n").length - 1,
    });
  }
}
