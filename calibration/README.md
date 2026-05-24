High level plan ideas (conversations with chat)(1).pdf
PDF
AI-Assisted_Vulnerability_Detection in_LLM-Generated_Code (2)(2).pdf
PDF
Ideas for Report Adjustments (conversations with chat).pdf
PDF
So, given that I wanna make adjustments to my experimentation, to my tool, through like calibration and stuff, I think I wanna design like a public repository so that I can start placing in there documents that I generate along the way, such as calibration logs, experiment logs, dataset information, the change log that we recommended. Things that are expected to be in a professional public repository. So basically, I will also be like I will be discussing, I'll be referring to the repository for more details, right? So when I talk about, for example, my experiments, I'm gonna say, for the details are on the repository, right? So I want this repository to look very professional. I want it to resemble real, you know, technologies that are professional and that are recognized, like from leading technology companies. So that when people look at this repository, they take it seriously and they're like, it has all of the information they need on there. And I feel like it's really important because a paper is just that, people need to see more details. And I feel like the repository is the sack of that. So I really wanna craft a repository that So can you please help me to design a repository? I feel like it's the main step I should work on because I also need to do other things like create the dataset, create my calibration plan and carry it out, the experimentation plan and carry it out, and then, you know, along the way, I'm going to generate documents. So, I want these documents to be what I'm going to have in this public repository with all the information that anybody reviewing my report should be able to see. So can you please help me to figure that out? Thank you. Help me figure out the best design for this repository. Thanks.

After reviewing the direction in your report, the high-level planning document, and the report-adjustment plan, I think you're thinking about the repository in exactly the right way. In fact, your own notes already point toward separating the tool from the evidence of the tool's effectiveness.

What I would recommend is something very similar to what mature research labs, AI companies, and security startups do:

Do NOT Think "Repository"

Think:

Project Ecosystem

For a professional project, there is rarely just one repository.

Instead there are:

1. Research Repository (Public)

Purpose:

Prove claims.

Contains:

Experiment logs
Calibration logs
Datasets
Results
Graphs
Methodology
Reproducibility information
Changelogs
Papers
Presentations

This is the repository people cite.

2. Product Repository (Private)

Purpose:

Actual implementation.

Contains:

LangGraph workflow
Internal prompts
Retrieval logic
Vector DB construction
Configuration files
Source code
Future versions

Nobody sees this.

3. Documentation Repository (Optional)

Purpose:

Professional project documentation.

Contains:

Architecture documents
Requirements
Design decisions
Future roadmap
Development notes

Can be private.

Sometimes eventually public.

What Leading Research Projects Actually Share

Look at many papers from:

Google Research
OpenAI
Anthropic
Microsoft Research
GitHub Security Lab

The paper often says:

Additional results available in repository.

But that repository usually contains:

datasets
benchmark results
evaluation scripts
figures
supplementary material

NOT proprietary implementation details.

This is very normal.

What I Would Build For Your Project

I would create a public repository called something like:

llm-security-evaluation

or

context-aware-security-evaluation

or

langgraph-security-benchmark

Notice:

The repository is about evaluation.

Not the tool.

Proposed Public Repository Structure
repository/

README.md

CHANGELOG.md

LICENSE

docs/
│
├── project_overview.md
├── methodology.md
├── calibration_strategy.md
├── experimental_setup.md
│
datasets/
│
├── securityeval/
├── generated_cases/
│
calibration/
│
├── rag/
│
├── prompts/
│
├── validation/
│
└── llm_selection/
│
experiments/
│
├── experiment1/
│
├── experiment2/
│
├── experiment3/
│
results/
│
├── figures/
│
├── tables/
│
└── raw_results/
│
reports/
│
├── paper.pdf
│
└── poster.pdf
│
appendix/
│
├── prompts_public.md
│
├── equations.md
│
└── reproducibility.md

This immediately looks professional.

Most Important Folder

Honestly:

calibration/

This is what most student projects completely lack.

Your revised report is moving heavily toward calibration-first methodology.

That means your repository should tell the story:

Observation
↓
Hypothesis
↓
Adjustment
↓
Calibration
↓
Result
↓
Final Design Decision

For example:

calibration/

rag/

C001_problem.md

Observation:
Missed CWE-1104

Hypothesis:
Retrieval lacks dependency context

Modification:
Added CVE relationship retrieval

Result:
Accuracy improved from X to Y

Decision:
Adopted for Version 1.2

Reviewers LOVE this.

Why?

Because it demonstrates engineering rigor.

The Single Most Professional Addition

Create:

decision_log.md

Inside:

Decision D-001

Date:
2026-06-01

Problem:
High false positives

Options:
4 runs
8 runs
12 runs

Chosen:
8 runs

Reason:
Best accuracy/latency tradeoff

Professional engineering teams do this constantly.

Versioning Strategy

You mentioned future versions.

Do not create new repositories for every version.

Instead:

Version 1.0
Prototype

Version 1.1
Improved validation

Version 1.2
Expanded RAG

Version 2.0
SecurityEval benchmark

Version 3.0
Graph-enhanced retrieval

Track them through:

CHANGELOG.md

and

releases/

folder.

Repository Storytelling

This is something many engineers miss.

When someone opens your repository they should immediately understand:

What problem exists?

README

Why does it matter?

Project overview

How was it evaluated?

Experiments

How was it calibrated?

Calibration

What changed?

Changelog

What were the results?

Results folder

Can I reproduce it?

Experimental setup

What comes next?

Roadmap

Repository Sections I Would Build First

Before touching anything else:

Priority 1
README.md
Priority 2
docs/project_overview.md

One-page summary.

Priority 3
CHANGELOG.md
Priority 4
docs/calibration_strategy.md

This aligns directly with the calibration section you plan to add before experiments.

Priority 5
experiments/

Skeleton structure only.

No results yet.

If This Were My Project

Knowing everything about your research direction, publication goals, SecurityEval expansion plans, calibration-first methodology, and desire to keep the architecture private, I would organize the ecosystem as:

GitHub Organization

AI-Security-Research/
│
├── security-evaluation-public
│      (public)
│
├── experiment-results
│      (public)
│
├── paper-materials
│      (public)
│
└── langgraph-security-engine
       (private)

The public side demonstrates rigor, reproducibility, and scientific credibility.

The private side protects the implementation, orchestration logic, prompts, retrieval pipeline, and future commercial value.

That structure is much closer to how a serious research effort or early-stage technology startup would organize itself than a single repository containing everything.

Yes. In fact, I would argue that before you run another calibration experiment or write another section of the paper, you should design the repository structure first.

Why?

Because every calibration, experiment, graph, table, observation, hypothesis, and result you generate from this point forward should have a predetermined home.

Otherwise you end up with exactly what happens in many research projects:

PDF_final_v2_REAL_FINAL.pdf

experiment_new_new_fixed.xlsx

calibration_notes_3.docx

And six months later nobody knows where anything came from.

My Recommendation

Think of the repository as:

The Evidence Repository

Not:

The Tool Repository

Your private repository is:

The Technology

Your public repository is:

The Evidence

The public repository exists to answer:

What problem was studied?
How was the system evaluated?
How was it calibrated?
What results were obtained?
Why were design decisions made?
Can the results be trusted?
The Repository Story

I would structure it so that a reviewer can read it in the same order as your paper.

Your report is evolving toward:

Introduction

↓

Architecture

↓

Calibration

↓

Experiment 1

↓

Experiment 2

↓

Experiment 3

↓

Discussion

↓

Future Work

The repository should mirror that structure.

Ultimate Repository Structure
llm-security-framework-evaluation/

README.md

CHANGELOG.md

LICENSE

CITATION.cff

------------------------------------------------

docs/

------------------------------------------------

project_overview.md

research_questions.md

architecture_summary.md

experimental_methodology.md

reproducibility.md

roadmap.md

------------------------------------------------

calibration/

------------------------------------------------

README.md

rag/

context/

validation/

prompts/

llm_selection/

------------------------------------------------

experiments/

------------------------------------------------

experiment1_securityeval/

experiment2_tool_comparison/

experiment3_end_to_end/

------------------------------------------------

results/

------------------------------------------------

experiment1/

experiment2/

experiment3/

summary_tables/

figures/

------------------------------------------------

datasets/

------------------------------------------------

securityeval/

generated_cases/

ground_truth/

------------------------------------------------

reports/

------------------------------------------------

paper_versions/

poster_versions/

slides/

------------------------------------------------

appendix/

------------------------------------------------

equations/

prompts/

tool_versions/

system_configs/

------------------------------------------------

archive/

------------------------------------------------

old_versions/

deprecated_calibrations/

This is honestly very close to how a mature university research lab would organize a publication project.

Section 1

README

Most important file.

When somebody lands on the repository they should immediately see:

Project Overview

Motivation

Research Questions

Architecture Overview

Experimental Design

Results Summary

Repository Structure

Reproducibility

Citation

The README should almost feel like a miniature version of your paper.

Section 2

docs/

This is where the intellectual story lives.

Not implementation.

Not code.

Examples:

project_overview.md

Explains:

problem
motivation
contribution
architecture_summary.md

Only high level.

Example:

Input

↓

Preprocessing

↓

RAG

↓

Detection

↓

Validation

↓

Fix Generation

↓

Reporting

No proprietary details.

No prompts.

No internal implementation.

experimental_methodology.md

Explains:

dataset
metrics
evaluation procedures

This will make your paper stronger because reviewers can inspect details separately.

Section 3

Calibration

This is where your repository becomes special.

Most student repositories do not contain this.

Your project should.

RAG Calibration
calibration/rag/

Examples:

RAG_C001.md

Observation

Hypothesis

Modification

Evaluation

Decision
Validation Calibration
validation/

Examples:

4 runs

8 runs

12 runs

Compare:

accuracy
latency
consistency
Context Calibration
context/

Examples:

code_only

code_plus_context

Compare:

accuracy
false positives
LLM Calibration
llm_selection/

Examples:

Configuration A

GPT-4

↓

GPT-4

↓

GPT-4

Configuration B

GPT-4

↓

Claude Opus

↓

Claude Sonnet

Results:

accuracy
latency
false positives
Section 4

Experiments

This should mirror your report exactly.

Experiment 1

SecurityEval Evaluation

experiments/
└── experiment1_securityeval/

Contains:

overview.md

dataset_description.md

execution_protocol.md

metrics.md

observations.md
Experiment 2

Tool Comparison

experiment2_tool_comparison/

Contains:

Bandit

CodeQL

Reference Method

Proposed Framework

Results:

accuracy
FPR
FNR
latency
Experiment 3

End-to-End Integration

experiment3_end_to_end/

Contains:

workflow_description.md

evaluation.md

integration_results.md

This experiment is likely one of your strongest future contributions because it connects directly to the EASE paper's secure development loop.

Section 5

Results

This becomes the repository's "gallery."

Example:

results/

experiment1/

experiment2/

experiment3/

summary_tables/

figures/

All graphs live here.

All tables live here.

This is what your report will reference repeatedly.

For example:

Detailed per-CWE results are available in the repository.

or

Additional calibration figures are available in the repository.

Section 6

Datasets

This will become critical once you move to SecurityEval and expanded evaluation.

Structure:

datasets/

securityeval/

generated_cases/

ground_truth/

Never mix datasets with experiment results.

Professional projects separate them.

Section 7

Appendix

This is where reproducibility lives.

Examples:

appendix/

equations/

tool_versions/

system_configs/

Examples:

CodeQL version
Bandit version
LangGraph version
Python version
Hardware specs

Exactly the type of information discussed in your planning notes.

The Most Valuable File

If I could add only one file beyond the README, it would be:

decision_log.md

Structure:

Decision ID

Date

Problem

Hypothesis

Alternatives

Chosen Solution

Justification

Evidence

Example:

Decision D-005

Problem:
False positives too high.

Hypothesis:
Validation runs reduce instability.

Alternatives:
4 runs
8 runs
12 runs

Chosen:
8 runs

Evidence:
Calibration V-003

Reason:
Best accuracy/latency tradeoff.

This file becomes the engineering history of the project.

My Final Recommendation

For your specific publication-oriented security research project, the repository should be organized around:

Problem
↓
Architecture
↓
Calibration
↓
Experiments
↓
Results
↓
Decisions
↓
Future Work

Not around source code.

Not around random folders.

Not around dates.

That structure creates a repository that looks like it belongs to a serious research effort and gives you a natural place to store every calibration log, experiment result, dataset description, graph, table, and design decision you generate during the next phase of the project.

perfect, I really like the idea and I think we should implement it. So now, can you give me the final design plan, not the implementation structure, but the ideal design? Because after you generate this for me, I'm going to ask for implementation instructions. So I guess first, before we do that, I want to have the ultimate design that we agree on. So I like the idea that you gave here, and now I would just like for you to organize this information into the final design for the repository. Thank you.

I agree. Before we discuss implementation, we should finalize the design philosophy. The structure itself is easy to change later; the design principles are what matter. Once those are correct, every folder, document, graph, and experiment naturally finds its place.

For your project, I would define the repository as follows:

Public Repository Design Philosophy
Purpose

This repository is not the tool.

This repository is the scientific evidence, evaluation history, and engineering justification for the tool.

Its purpose is to demonstrate:

What problem was studied
Why the problem matters
How the system evolved
How design decisions were made
How experiments were conducted
What results were achieved
Why those results should be trusted
How future researchers can reproduce the evaluation

The repository does not reveal proprietary implementation details.

The repository documents the research journey and the evidence supporting the claims.

Core Principle

The repository should tell a complete story.

A reviewer should be able to start at the beginning and understand:

Problem

↓

Motivation

↓

Architecture Concept

↓

Calibration

↓

Experiments

↓

Results

↓

Conclusions

↓

Future Directions

without needing access to the private implementation.

What Makes This Repository Different

Most student repositories contain:

Source code
Random screenshots
Final report

and little else.

This repository will function more like the supplementary materials repository of a serious research project.

The emphasis is not on code.

The emphasis is on:

Evidence
Reproducibility
Engineering Decisions
Experimental Rigor
Scientific Transparency
Repository Identity

The repository should represent:

Versioned Scientific Evaluation

rather than

Versioned Software

The private repository tracks software evolution.

The public repository tracks evidence evolution.

That distinction is extremely important.

Organizational Narrative

The repository should follow a logical narrative.

1. Project Foundation

Why does this project exist?

Includes:

project overview
motivation
research questions
references to related work

This establishes context.

2. Architecture Overview

What is the high-level approach?

Includes:

workflow diagrams
conceptual architecture
component descriptions
assumptions

High-level only.

No proprietary implementation.

The purpose is understanding.

Not replication.

3. Calibration

Why was the architecture designed this way?

This becomes one of the strongest parts of the repository.

Every important design decision should be justified through evidence.

Each calibration follows:

Observation

↓

Hypothesis

↓

Adjustment

↓

Evaluation

↓

Decision

This demonstrates engineering discipline.

4. Experimental Evaluation

How was the system tested?

Experiments become the center of the repository.

For your project:

Experiment 1

SecurityEval evaluation

Experiment 2

Tool comparison

Experiment 3

End-to-end integration

Each experiment should contain:

Purpose

Methodology

Metrics

Results

Analysis

Limitations

5. Results Archive

The repository becomes the permanent home of:

detailed tables
graphs
per-case outputs
calibration measurements
supplementary results

The paper summarizes findings.

The repository stores the evidence.

6. Reproducibility

A professional repository explains:

dataset sources
evaluation methodology
software versions
hardware configuration
metrics definitions

Someone should understand exactly how the evaluation was performed.

7. Evolution History

One of the most important sections.

The repository should document:

how the tool changed
why it changed
what evidence motivated the change

Not just:

Version 1

Version 2

but:

We observed X

We hypothesized Y

We tested Z

Therefore we adopted configuration A

This is how serious engineering organizations justify decisions.

Guiding Principles for Every Document

Every document should answer one question.

Examples:

Calibration document:

Why was this adjustment made?

Experiment document:

How was this experiment conducted?

Result document:

What was observed?

Decision document:

Why was this design selected?

If a document does not answer a clear question, it probably does not belong.

Relationship to the Paper

The paper becomes:

Concise Scientific Narrative

The repository becomes:

Detailed Supporting Evidence

The paper should repeatedly be able to say:

Detailed calibration results are available in the repository.

Additional experiment outputs are available in the repository.

Full evaluation logs are available in the repository.

This increases credibility without overcrowding the paper.

Relationship to Future Versions

The repository should support multiple generations of the project.

Not just the current version.

Future versions should build upon previous evidence.

For example:

Version 1:

baseline architecture
initial calibration
first SecurityEval evaluation

Version 2:

improved retrieval
expanded benchmark coverage
updated experiments

Version 3:

advanced context engineering
GraphRAG integration
broader evaluation

The repository becomes a historical record of scientific progress.

Desired Impression

When a professor, researcher, conference reviewer, company engineer, investor, or collaborator opens the repository, the reaction should be:

This project is organized.

The claims are supported.

The methodology is documented.

The experiments are reproducible.

The design decisions are justified.

The work is being conducted professionally.

Not:

This is a collection of files.

Not:

This is just a code repository.

The repository should feel like the public research and evaluation archive of a serious technology project.

Final Repository Vision

In one sentence:

The repository is the public scientific record of the evolution, calibration, experimentation, validation, and evaluation of the AI-assisted vulnerability detection framework, while the private repository remains the home of the proprietary implementation and future product development.

I think this design aligns extremely well with your goals of:

expanding to the SecurityEval benchmark,
performing calibration before experimentation,
comparing against Bandit, CodeQL, and the reference methodology,
documenting architectural evolution,
supporting future publications,
preserving intellectual property,
and eventually evolving the project beyond a university prototype into a more mature research or commercial effort.
All right, now I would like for you to help me create this repository. So I would like for you to give me a step-by-step, click-by-click instructions to create this design you just recommended. Please, thank you.

Yes — here is the clean step-by-step plan.

Step 1: Create the Public Repository
Go to GitHub.
Click the + icon in the top-right.
Click New repository.
Repository name:
llm-security-framework-evaluation
Description:
Public evaluation repository for an AI-assisted, context-aware vulnerability detection framework.
Set visibility to Public.
Check Add a README file.
Add .gitignore: choose Python.
License: choose MIT only if you are comfortable allowing reuse. Otherwise choose No license for now.
Click Create repository.
Step 2: Create the Main Folders

In your new GitHub repo:

Click Add file.
Click Create new file.
In the filename box, type:
docs/.gitkeep
Click Commit changes.

Repeat this same process for each folder:

calibration/.gitkeep
experiments/.gitkeep
results/.gitkeep
datasets/.gitkeep
reports/.gitkeep
appendix/.gitkeep
archive/.gitkeep

This creates the main structure.

Step 3: Create the Detailed Folder System

Now create these placeholder files the same way:

calibration/rag/.gitkeep
calibration/context/.gitkeep
calibration/validation/.gitkeep
calibration/prompts/.gitkeep
calibration/llm_selection/.gitkeep
experiments/experiment1_securityeval/.gitkeep
experiments/experiment2_tool_comparison/.gitkeep
experiments/experiment3_end_to_end/.gitkeep
results/experiment1/.gitkeep
results/experiment2/.gitkeep
results/experiment3/.gitkeep
results/summary_tables/.gitkeep
results/figures/.gitkeep
datasets/securityeval/.gitkeep
datasets/generated_cases/.gitkeep
datasets/ground_truth/.gitkeep
reports/paper_versions/.gitkeep
reports/poster_versions/.gitkeep
reports/slides/.gitkeep
appendix/equations/.gitkeep
appendix/prompts/.gitkeep
appendix/tool_versions/.gitkeep
appendix/system_configs/.gitkeep
archive/old_versions/.gitkeep
archive/deprecated_calibrations/.gitkeep
Step 4: Create the Core Documents

Create these files at the root level:

CHANGELOG.md
decision_log.md
CITATION.cff

Create these inside docs/:

docs/project_overview.md
docs/research_questions.md
docs/architecture_summary.md
docs/experimental_methodology.md
docs/reproducibility.md
docs/roadmap.md

Create these inside calibration/:

calibration/README.md
calibration/calibration_template.md

Create these inside experiments/:

experiments/README.md
experiments/experiment_template.md
Step 5: Recommended Final Repository Layout

Your repository should eventually look like this:

llm-security-framework-evaluation/

├── README.md
├── CHANGELOG.md
├── decision_log.md
├── CITATION.cff
├── .gitignore
│
├── docs/
│   ├── project_overview.md
│   ├── research_questions.md
│   ├── architecture_summary.md
│   ├── experimental_methodology.md
│   ├── reproducibility.md
│   └── roadmap.md
│
├── calibration/
│   ├── README.md
│   ├── calibration_template.md
│   ├── rag/
│   ├── context/
│   ├── validation/
│   ├── prompts/
│   └── llm_selection/
│
├── experiments/
│   ├── README.md
│   ├── experiment_template.md
│   ├── experiment1_securityeval/
│   ├── experiment2_tool_comparison/
│   └── experiment3_end_to_end/
│
├── results/
│   ├── experiment1/
│   ├── experiment2/
│   ├── experiment3/
│   ├── summary_tables/
│   └── figures/
│
├── datasets/
│   ├── securityeval/
│   ├── generated_cases/
│   └── ground_truth/
│
├── reports/
│   ├── paper_versions/
│   ├── poster_versions/
│   └── slides/
│
├── appendix/
│   ├── equations/
│   ├── prompts/
│   ├── tool_versions/
│   └── system_configs/
│
└── archive/
    ├── old_versions/
    └── deprecated_calibrations/
Step 6: Do Not Upload These Publicly

Keep these private:

source code
internal prompts
API keys
vector database files
private architecture details
private LangGraph node logic
full proprietary workflow implementation
Step 7: What To Add First

After the folders exist, fill these first:

README.md
docs/project_overview.md
docs/architecture_summary.md
calibration/README.md
experiments/README.md
decision_log.md
CHANGELOG.md

This gives you a professional public foundation before adding results.

Experiment Plan.pdf
PDF
Dataset generation plan.pdf
PDF
Calibration Plan.pdf
PDF
AI-Assisted_Vulnerability_Detection in_LLM-Generated_Code (3).pdf
PDF
Perfect. Now, I have created the repository. Now, I need to do step 7. And I have attached here some documents for you to reference because I want you to create for me all of these documents you recommend for step 7. And I want to create them one by one. So we'll begin with the README. And again, to generate them, I would like for them to be very professional, so whenever anybody reads my report and there are references to my repository, all of these documents need to be very professional, very serious, very honest. Everything needs to be, you know, given professionalism. So therefore, I want you to help me create them with that in mind because I want my idea to be taken seriously, to be truly considered, and therefore all of these things matter. The presentation of the repository needs to be very professional. Everything needs to be organized and, you know, clear to follow through and understand. So even though there is not my method in this repository, which is completely fair, it's not necessary to be there, but all of these documents need to be able to make the audience really understand my project and provide, you know, support and evidence for all of my claims and my... report. Ultimately, I am trying to create a very professional report, and part of the report is the repository that you reference. So therefore, I want these documents to be very professional and give a very great impression. So therefore, I have attached in here some documents that you have helped me create, like the experiment plan, calibration plan, dataset generation plan, and my current report, which overall summarizes the progress I have made up until now. So I want you to help me, let's first discuss how we should create the documents if we want to have them look very professional. Because also when I share my report with my professor, I will let him know about the adjustments I made, and I will tell him things like, oh, I added references to my repository, and I think on there I will add, like, here is the link to my repository if you would like to look at it, which I think you would, of course. So I want to make sure that this repository, it's really professional and impressive. So please help me discuss how we can achieve that. So I feel like for my project to give off a very great impression and to be very impressive and taken serious, it needs to kind of resemble, you know, how established organizations do it. They have clean repositories, they have professional reports, novel, and... value research delivered at the right time, et cetera. So before we generate these documents, I would like for you to give me any insight, advice on how I can take my project to that level to be taken serious, to not be, you know, seen as something that is not that impressive, all the opposite. I want my project to truly be up to the level of, you know, recognized organizations, recognized researchers, recognized innovators. So what is your advice there? I know that adding a very professional repository, polishing my report, expanding experimentation, and all these things I'm trying to do are helping in that sense, but what other things could be helpful? What other things would leading innovators take into account? Let's be brief about it, but also please help me out. Ultimately, I want that when I share this with my professor, with the world, everything gives off seriousness, professionalism, a great impression, and ultimately that interest to consider this, you know, to be something valuable in the real world. That way, there is that consideration for, you know, potential business. Of course, I don't wanna mention that anywhere. Again, there is the tone for humility that matters a lot, but I feel like the presentation of your report, your repository, the relevance of your research, and your great commitment to truly providing something valuable to contributing by providing solutions is what leads to that interest, right? Not necessarily having an inflated ego, being arrogant, overselling, overclaiming. All those things don't really help in that sense. They more lead to questioning and doubt and, you know, overall not support, whereas all these other things like having a really professional, impressive, easy-to-follow-through repository and very professional, impressive report, relevant research, and all these things, they sell that more than having some elevated tone, right? So please help me out with that before we generate the documents. Thank you.

After reviewing the report, calibration plan, dataset plan, and experiment plan, I think you're focusing on exactly the right things.

What stands out most is not the architecture itself. It is the direction of the project:

You identified a real problem (security weaknesses in AI-generated code).
You grounded the work in prior literature rather than inventing a benchmark.
You are moving toward SecurityEval for reproducibility and broader CWE coverage.
You have a calibration-first methodology rather than immediately running experiments.
You are planning multiple experiments that answer specific research questions instead of collecting random results.

Those are the characteristics reviewers usually associate with serious research.

What Actually Makes Research Look Professional

Many students think:

fancy diagrams
large architecture
complicated terminology

create credibility.

In reality, the strongest signal is:

Evidence-Based Decision Making

Every design choice should have a reason.

For example:

Bad:

We switched retrieval methods because it sounded better.

Good:

Calibration revealed retrieval noise and contextual ambiguity, motivating a hybrid retrieval strategy.

One sounds like experimentation.

The other sounds like engineering.

The Biggest Difference Between Student Projects and Professional Projects

Student project:

Build system → run experiment → report result.

Professional project:

Observe problem → formulate hypothesis → test adjustment → document outcome → justify decision.

Your repository should emphasize this process everywhere.

That is why I keep recommending:

calibration logs
decision logs
changelog
experiment plans

because they show how conclusions were reached.

What Leading Research Organizations Care About

When researchers at places like:

Google Research
Microsoft Research
Anthropic
OpenAI

evaluate a project, they typically ask:

Is the problem important?
Is the methodology sound?
Are claims supported by evidence?
Are limitations acknowledged?
Can the work be reproduced?
Is there a clear future direction?

Interestingly, they care far less about whether the current prototype is perfect.

One Thing You Already Do Well

You consistently avoid claiming:

100% accuracy

perfect detection

solves cybersecurity

Instead, your report openly discusses:

retrieval limitations
contextual ambiguity
dependency reasoning issues
prompt sensitivity
scalability concerns

That honesty increases credibility.

Professional reviewers generally trust papers that acknowledge weaknesses more than papers that claim perfection.

What Would Impress a Professor Most

Not:

I built a revolutionary AI system.

But:

I identified a meaningful problem, developed a structured methodology, evaluated it carefully, documented limitations, and proposed evidence-based future improvements.

Your current direction is already moving toward that.

What I Would Focus On Next

Before worrying about making the repository "impressive," focus on making it:

Organized

Every document has a clear purpose.

Consistent

Same terminology throughout.

Reproducible

Readers understand exactly what was done.

Traceable

Results can be linked back to experiments.

Honest

Claims match evidence.

If you achieve those five things, the repository will naturally feel professional.

My Recommendation Before Writing The README

Before generating the actual README, I would establish three guiding principles for every repository document:

Principle 1

Evidence over claims.

Whenever possible:

Show results.

Show methodology.

Show reasoning.

Not marketing language.

Principle 2

Documentation over complexity.

Simple architecture clearly explained is stronger than a complicated architecture poorly explained.

Principle 3

Transparency over perfection.

Document:

successes
failures
calibration outcomes
limitations
future work

This creates trust.

What I Think Your Repository Should Feel Like

If somebody visits your repository after reading the paper, they should feel:

This project is organized.

The methodology is thoughtful.

The author understands the limitations.

The experiments are structured.

The work appears reproducible.

The project is actively evolving through documented calibration and experimentation.

That impression is much more valuable than trying to make the project appear larger, more complex, or more revolutionary than it currently is.

And based on the report, calibration plan, dataset plan, and experiment roadmap you've assembled, the strongest path forward is not to exaggerate the novelty of the system—it is to demonstrate rigor, transparency, organization, and systematic improvement through calibration and experimentation.

The next document I would create is the README.md, because it becomes the front door to everything else in the repository. Once the README is finalized, the remaining documents (project overview, architecture summary, calibration overview, experiments overview, changelog, and decision log) can all inherit the same tone and structure.

Perfect. This was great. Thank you very much. Now, let's create the README, please. Thank you.

Excellent. Based on your report, dataset plan, calibration plan, experiment roadmap, and the repository philosophy we established, I would make the README look like something you would realistically see attached to a university research project, research lab prototype, or early-stage security research effort. It should be professional, factual, organized, and avoid overselling. The goal is that a professor, researcher, engineer, or future collaborator can understand the project in five minutes.

I would recommend using the following as your initial README.md:

AI-Assisted Vulnerability Detection in LLM-Generated Code
Overview

This repository contains the public evaluation, calibration, experimentation, and documentation materials associated with the research project:

"AI-Assisted Vulnerability Detection in LLM-Generated Code: A LangGraph-Orchestrated Workflow for Context-Aware Vulnerability Detection and Secure Code Fixing."

The project investigates whether structured orchestration, retrieval-augmented security knowledge, contextual reasoning, repeated validation, and remediation generation can improve the reliability of vulnerability detection in AI-generated software.

The repository serves as the public research and evaluation archive for the project. It documents the methodology, calibration process, experimental design, results, and architectural evolution used throughout development while intentionally excluding proprietary implementation details.

Motivation

Recent advances in large language models have significantly accelerated software development by enabling automated code generation and AI-assisted programming workflows.

However, research has shown that AI-generated code can contain security vulnerabilities, including weaknesses that depend heavily on contextual understanding, authorization behavior, workflow semantics, operational assumptions, and business logic.

Traditional static-analysis tools such as Bandit and CodeQL remain highly valuable for detecting many vulnerability patterns, but certain security issues require deeper contextual interpretation.

This project explores whether an orchestration-oriented workflow can improve contextual vulnerability analysis by combining:

Structured security context
Retrieval-augmented security knowledge
LLM-based vulnerability reasoning
Repeated validation
Secure code remediation
Structured reporting
Research Objectives

The project investigates the following research questions:

RQ1 – Contextual Vulnerability Reasoning

Can the framework improve detection of vulnerabilities that depend on authorization behavior, workflow semantics, business logic, or operational context?

RQ2 – Comparative Detection Performance

How does the framework compare against traditional security-analysis tools such as Bandit and CodeQL?

RQ3 – Retrieval-Augmented Reliability

Does integrating external security knowledge improve vulnerability-analysis consistency and explainability?

RQ4 – Architectural Evolution

How do orchestration-oriented components evolve through iterative experimentation and calibration?

High-Level Architecture

The framework follows a multi-stage LangGraph-orchestrated workflow:

Input
↓
Preprocessing
↓
Security Knowledge Retrieval (RAG)
↓
LLM Vulnerability Detection
↓
Validation
↓
Fix Generation
↓
Structured Reporting

The workflow combines source code, contextual security information, vulnerability knowledge retrieval, LLM reasoning, repeated validation, remediation generation, and explainable reporting into a unified vulnerability-analysis pipeline.

This repository provides high-level architectural descriptions only. Detailed implementation components remain private.

Repository Purpose

This repository is designed to document:

Calibration methodology
Experimental methodology
Dataset construction
Evaluation procedures
Results and visualizations
Architectural evolution
Design decisions
Reproducibility information

The repository does not contain proprietary source code, internal orchestration logic, private prompts, deployment infrastructure, or implementation-specific intellectual property.

Calibration Strategy

Prior to large-scale experimentation, the framework undergoes a structured calibration phase focused on improving:

Security context engineering
Retrieval quality
Prompt design
Validation consistency
Explainability

The calibration process follows an evidence-driven workflow:

Observation
↓
Hypothesis
↓
Adjustment
↓
Evaluation
↓
Decision

Calibration documentation can be found in the calibration/ directory.

Experimental Roadmap

The project currently includes three major experimental studies.

Experiment 1 – Safe vs Vulnerable Classification

Evaluate the framework's ability to classify secure and vulnerable implementations across a SecurityEval-derived dataset spanning multiple CWE categories.

Primary metrics:

Accuracy
False positives
False negatives
Confidence
Retrieval quality
Latency
Experiment 2 – Tool Comparison

Compare the framework against:

Bandit
CodeQL
Published results from prior end-to-end secure code agent research

The focus is not on proving universal superiority, but on understanding the strengths and limitations of different security-analysis approaches.

Experiment 3 – End-to-End Workflow Integration

Evaluate the framework as a security-review component within an AI-assisted secure-code-generation workflow inspired by prior secure-code-agent research.

The goal is to assess how contextual retrieval, validation, and structured remediation contribute to the overall secure-development process.

Dataset

The experimental dataset is derived from SecurityEval methodology and expanded to support:

Vulnerable samples
Secure samples
Ground-truth CWE labels
Security context profiles

The dataset design emphasizes reproducibility, broader CWE coverage, and compatibility with contextual retrieval workflows.

Dataset documentation is available in the datasets/ directory.

Current Status

Current development efforts focus on:

Repository organization
Calibration execution
SecurityEval dataset construction
Expanded CWE coverage
Retrieval improvements
Experimental preparation

Future work includes:

Hybrid retrieval refinement
Expanded benchmark evaluation
End-to-end workflow integration
Model comparison studies
Additional contextual vulnerability categories
Reproducibility

The repository documents:

Experimental methodology
Dataset generation procedures
Calibration decisions
Evaluation metrics
Tool configurations
Software versions

Detailed reproducibility information is available throughout the repository documentation.

Repository Structure
docs/
calibration/
experiments/
results/
datasets/
reports/
appendix/
archive/

Additional documentation describing the purpose of each section is provided within the corresponding directories.

Disclaimer

This repository is intended for research and educational purposes.

The project remains an active research effort. Experimental results, calibration findings, architectural decisions, and documentation may evolve as additional evaluation and validation are completed.

Citation

Citation information will be provided following publication or formal release of the research report.

Why I like this README:

It sounds like a research project, not a startup pitch.
It avoids unsupported claims.
It aligns with the paper, calibration plan, dataset plan, and experiment roadmap.
It establishes credibility through methodology and organization rather than marketing language.
It provides a professional front page that a professor, researcher, or engineer can immediately understand.
Perfect. Now, I think that the research questions we had might need to change slightly because now that we're going to carry out experiment 3, we have to have a question that asks about something like, how does the integration of this framework affect the end-to-end loop, something like that. And I also think that for the current questions 3 or 4, maybe those belong more in the first questions because they are more focused on figuring out the value of the components, such as the RAG, retrievalment of reliability, and the other components. And I feel like for the story of the report, we are first gonna do like the calibration things and then go to the experiments. So I feel like maybe we need to reorder the questions so that it aligns with that story. So maybe the first question is something more about the architectural evolution and architecture and contributions. So maybe question 3 or 4 could be merged in some way to sound more like, how do the orchestration-oriented components evolve and contribute? to the effectiveness of the tool, something like that. And that question should be more about, you know, related to the calibration, right? It needs to overview the purpose of performing the calibration. That way, that question is associated with justifying the architecture. Basically asking, why is this architecture valid? Like, how is it helpful, right? Before we dive into the experiments and further prove why it was helpful. So I think I would need to reorder the questions and adjust them slightly. So I think question, the current question one and two should become question two and three, and then we need a fourth question that is about the third experiment. So ultimately, I need four questions, and I want the current question three and four to be merged into one question, like I've been discussing, to overall overview the calibration process. And that question needs to become question one. And then the next questions would be for question two, that would be contextual vulnerability reasoning, question three would be comparative detection performance, and then question four would be integration into the end-to-end loop. So please help me to validate that idea and help me come up with the questions. And then after that, I think we can regenerate this readme so that it's more aligned with that direction, because these questions guide a lot of, you know, everything. So please help me figure that out, and then we'll discuss anything further if needed, and then we'll generate the readme once again. Thank you.Also, I'm not sure about mentioning things like detailed implementation components remain private. And then when we say the repository does not contain proprietary source code, da-da-da, proprietary, I mean property. I feel like those things kind of sound defensive, like we don't wanna share the details. Is there a way that we can rephrase that so it doesn't come off a little bit like, I don't know, defensive? Like maybe we just explain this repository purpose and then slightly add some sentence that says, the detailed implementation components are not included in this public repository, something like that. I feel like it sounds way more nice, right? We don't want language that sounds like, I don't know, negative, argumentative. I just want the language to be very polite. That matters a lot. And I think saying things like, detailed implementation components remain private, or the repository does not contain proprietary, da-da-da, property. I don't know, but I feel like it sounds a little too dramatic for barely even being considered. Like, openly being defensive about sharing your method at this stage, it's kind of silly because you're first trying to put it out there. So being so defensive about sharing your method is like... it's kind of silly, like, you need to be considered first. So I just think it's about changing the tone, right? So I think saying something more like, Detailed implementation components are, I don't know, I don't know how to say it. Maybe we just say something like, this repository provides high-level architectural descriptions, or this public repository provides the high-level architectural descriptions. And that's it. That hints to the fact that there is some other repository, right? And that's it. Let me know what you think on that. I just really care about the tone. Tone is so important for people to even listen. And to even, to be trying to get an idea to be considered, you need to have a very polite and humble tone, rather than defensive and argumentative and cocky, arrogant, whatever. The tone, humble, humble, and collaborative, contributive, aiming to contribute, not necessarily trying to be arrogant with, you know, thinking you've developed the next big thing. It's more about having the true energy to contribute. So I really care about that tone in the things I have produced. Thank you.Also, for the current status and future work, I feel like you got it wrong because now we're gonna be having the model comparison studies, we are gonna integrate into the end-to-end workflow, we are gonna expand the benchmark evaluation, we are gonna do the hybrid retrieval refinement, and we are gonna expand to additional contextual vulnerability categories. So the future work that you mentioned here, it's actually things that we're gonna take care of now. So maybe you could adjust that for me, please. Please do that. And then for the future work, I think we could say things like, I don't know, maybe I want to experiment with real program scenarios, right, not just single vulnerabilities, so that I can test, you know, real programs. And um maybe I also want to expand the RAG design and, you know, any other things that may be helpful. Like maybe in the future, tuning the models, right, like adjusting parameters or whatever. I don't know, I'm not so sure. But obviously, there is gonna be future work. But that needs to be adjusted because we are gonna be carrying out these things. So please help me figure that out before we generate the new readme. Thank you.So, when you mentioned the citation part, I don't wanna say that sentence you made. I don't know, it sounds like, like we are not adding citations in this report. I don't even know what to say about that part but i think citation information should be provided. does that mean i need to add maybe a folder containing the references? is thst how professional research papers, like reference 2 on my report, would approach that? please help me discuss all these things before implementing them and any other advice you may have. thank you

I think your instincts are correct on almost every point.

What you're doing here is not merely editing wording. You're refining the story of the research.

And the story matters tremendously.

A strong paper is not:

Architecture → Experiments → Results

A strong paper is:

Problem → Architectural reasoning → Calibration and refinement → Evaluation → Comparison → Real-world integration → Future directions

That is much closer to how mature research projects are presented.

1. I Agree With Reordering the Research Questions

Currently, your questions are:

RQ1 Contextual Vulnerability Reasoning
RQ2 Comparative Detection Performance
RQ3 Retrieval-Augmented Reliability
RQ4 Architectural Evolution and Refinement

The problem is that RQ3 and RQ4 are really about:

Why this architecture exists and how it evolved.

Those questions naturally belong before the experiments.

That aligns perfectly with the calibration phase you are introducing.

My Recommended Research Questions
RQ1 – Architectural Calibration and Evolution

How do orchestration-oriented architectural components—including contextual grounding, retrieval augmentation, prompt engineering, and validation strategies—evolve through calibration, and how do they contribute to the effectiveness of LLM-based vulnerability analysis?

Why I like it:

Covers calibration
Covers architecture evolution
Covers retrieval
Covers validation
Covers prompt engineering
Justifies architectural decisions
Creates a bridge into experiments

This becomes the foundation of the paper.

RQ2 – Contextual Vulnerability Reasoning

To what extent can the proposed framework identify vulnerabilities that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, or business logic?

This becomes Experiment 1.

RQ3 – Comparative Detection Performance

How does the proposed framework compare with traditional static-analysis tools and prior secure-code-agent methodologies across diverse vulnerability categories?

This becomes Experiment 2.

I would broaden it slightly beyond Bandit and CodeQL because you're also comparing against the EASE paper methodology.

RQ4 – End-to-End Workflow Integration

How does integrating the proposed framework into an AI-assisted secure-code-generation workflow influence vulnerability detection, remediation quality, and overall security outcomes?

This becomes Experiment 3.

And now the research questions align almost perfectly with:

Calibration
↓
Experiment 1
↓
Experiment 2
↓
Experiment 3

which is exactly the story you want.

2. I Completely Agree About the Tone

You made an excellent observation.

When I wrote:

Detailed implementation components remain private.

or

The repository does not contain proprietary implementation details.

it technically communicates the right idea.

But emotionally it feels defensive.

Almost as if the repository is apologizing for what it doesn't contain.

You don't want that.

Professional organizations usually don't emphasize what they're withholding.

They simply describe what the repository provides.

For example:

Instead of:

Detailed implementation components remain private.

I would write:

This repository provides high-level architectural descriptions, experimental methodology, calibration documentation, and evaluation results associated with the project.

Simple.

Positive.

Professional.

No defensiveness.

No emphasis on secrecy.

Readers naturally understand there are additional implementation artifacts elsewhere.

3. Current Status Section Needs Updating

You're absolutely right.

The previous version reflected work that was still future work.

But according to the calibration plan, dataset plan, and experiment plan, those are now planned deliverables.

Therefore:

Current Development Focus

Should become:

SecurityEval-derived dataset creation
Security context profile generation
Calibration execution
Hybrid retrieval refinement
Validation methodology documentation
Model configuration evaluation
Expanded CWE coverage
Experiment execution
Comparative evaluation
End-to-end workflow integration

Those are active work streams.

Not future work.

4. What Future Work Should Actually Be

I agree with your suggestions.

Future work should be beyond the scope of the current project.

Examples:

Real-World Software Evaluation

Move beyond isolated benchmark tasks and evaluate larger software systems.

Expanded Security Knowledge Graphs

Investigate GraphRAG and relationship-aware vulnerability retrieval.

Code-Aware Retrieval Models

Explore code-specialized embeddings and retrieval systems.

Multi-Language Support

Expand beyond Python-focused evaluation.

Adaptive Context Engineering

Automatically generate and refine contextual security profiles.

Human-in-the-Loop Security Review

Combine orchestration with developer feedback loops.

Production Pipeline Integration

Evaluate integration within real software development environments.

Fine-Tuning and Specialized Security Models

Investigate task-specific adaptation for vulnerability reasoning.

That feels like genuine future work.

Not things you're about to do next month.

5. The Citation Section

You raised a very good point.

I would not write:

Citation information will be provided after publication.

It sounds unfinished.

For research repositories, there are generally three approaches.

Option A (Recommended)

Create:

references/

folder

Inside:

references/

bibliography.bib

references.md

Then README says:

References used throughout the project are documented in the references directory.

Professional.

Simple.

Immediate.

Option B

Maintain:

docs/references.md

containing major papers:

Copilot paper
EASE paper
CWE
CVE
LangGraph references
RAG references

Also perfectly acceptable.

Option C

Use GitHub's:

CITATION.cff

This tells people how to cite your repository.

Useful later.

Not urgent right now.

My Biggest Recommendation Before Regenerating README

I would make one conceptual shift.

Current README feels like:

Here is my repository.

I would change it toward:

Here is the public research archive supporting this project.

That subtle change makes it feel much closer to:

university research labs
Microsoft Research repositories
benchmark repositories
supplementary material repositories

rather than a software project repository.

And I think that matches your goals perfectly.

The repository is not the product.

The repository is the evidence, methodology, calibration history, datasets, experiments, and results that support the research contribution. That framing is more mature, aligns with the calibration-first direction we discussed, and naturally creates the humble, collaborative, contribution-oriented tone you're aiming for.

I think I wanna generate the readme with these adjustments, and also for the references, I would like to go with option A. And everything else you mentioned, it's also good. Also, I do like the tone change. I think I wanna write the sentence you wrote, this repository provides high-level architectural descriptions, da-da-da, results associated with the project. It is simple, positive, professional, and non-defensiveness, or emphasis on secrecy. So basically, with all this, we have discussed and the recommendations, I think, oh, and also, I did like the questions. I feel like they are much more connected to the flow of the repository and the expanded experiments, and I think they are perfect. Also, I would like to mention that I am really concerned with crafting this document to the best of my ability, because when I regenerate my final report, I will very likely use many or all of these documents we generate to decide on the adjustments for the report. Therefore, the information we create here needs to be the kind of information I wanna see and the kind of information that is professional and what will be useful for using in the report when we go to create it. It will be the supporting documents. So yeah, can you please regenerate the readme now with the adjustments? Thank you.

I think this revised direction is significantly stronger than the previous README.

The biggest improvement is not the wording itself. It is that the README now aligns with the actual research narrative:

Motivation
↓
RQ1 Architecture & Calibration
↓
RQ2 Contextual Reasoning
↓
RQ3 Comparative Evaluation
↓
RQ4 End-to-End Integration
↓
Future Directions

That structure now mirrors:

the calibration plan,
the dataset plan,
the experiment roadmap,
and the future version of the paper.

That consistency is exactly what professional projects strive for.

I would recommend the following as the new README.md.

AI-Assisted Vulnerability Detection in LLM-Generated Code
Overview

This repository serves as the public research archive for the project:

AI-Assisted Vulnerability Detection in LLM-Generated Code: A LangGraph-Orchestrated Workflow for Context-Aware Vulnerability Detection and Secure Code Fixing

The project investigates how orchestration-oriented workflows combining contextual grounding, retrieval-augmented security knowledge, large language model reasoning, validation strategies, and remediation generation can support more reliable vulnerability analysis of AI-generated software.

The repository documents the calibration process, experimental methodology, datasets, evaluation results, architectural evolution, and supporting materials associated with the project.

Motivation

Artificial intelligence has rapidly become an important component of modern software development. Large language models can generate functional source code, accelerate prototyping, and assist developers throughout the software engineering lifecycle.

However, recent research has shown that AI-generated code may contain security vulnerabilities, including weaknesses that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, and business logic. Traditional static-analysis tools remain highly effective for many vulnerability categories, but certain security problems require deeper contextual reasoning.

This project explores whether a structured orchestration framework can improve vulnerability detection, explanation quality, remediation guidance, and workflow-level security analysis by combining retrieval-augmented security knowledge with contextual LLM reasoning and validation-oriented workflows.

Research Questions

The project investigates four primary research questions.

RQ1 – Architectural Calibration and Evolution

How do orchestration-oriented architectural components—including contextual grounding, retrieval augmentation, prompt engineering, and validation strategies—evolve through calibration, and how do they contribute to the effectiveness of LLM-based vulnerability analysis?

This question motivates the calibration phase and investigates how architectural refinements influence vulnerability-analysis performance, explainability, and reliability.

RQ2 – Contextual Vulnerability Reasoning

To what extent can the proposed framework identify vulnerabilities that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, or business logic?

This question evaluates the framework's ability to reason about vulnerabilities that extend beyond recognizable syntax-level patterns.

RQ3 – Comparative Detection Performance

How does the proposed framework compare with traditional static-analysis tools and prior secure-code-agent methodologies across diverse vulnerability categories?

This question investigates the relative strengths and limitations of orchestration-based vulnerability analysis compared with established approaches.

RQ4 – End-to-End Workflow Integration

How does integrating the proposed framework into an AI-assisted secure-code-generation workflow influence vulnerability detection, remediation quality, and overall security outcomes?

This question examines the role of the framework within broader secure-development workflows and end-to-end code-generation pipelines.

High-Level Framework Overview

The proposed framework follows a multi-stage orchestration workflow:

Input
↓
Preprocessing
↓
Security Knowledge Retrieval
↓
LLM Vulnerability Detection
↓
Validation
↓
Fix Generation
↓
Structured Reporting

The workflow combines source code, contextual security information, external vulnerability knowledge, vulnerability reasoning, validation mechanisms, remediation generation, and explainable reporting into a unified analysis pipeline.

This repository provides high-level architectural descriptions, experimental methodology, calibration documentation, and evaluation results associated with the project.

Repository Objectives

This repository is intended to:

Document architectural evolution and calibration activities
Provide experimental methodology and evaluation procedures
Maintain dataset documentation and generation protocols
Archive experimental results and supporting visualizations
Record design decisions and project milestones
Support reproducibility and transparency
Serve as a companion resource to the research report

The repository functions as the public documentation and evaluation archive supporting the project.

Calibration Strategy

Prior to expanded experimentation, the framework undergoes a structured calibration phase focused on improving:

Security context engineering
Retrieval quality
Contextual grounding
Prompt design
Validation consistency
Explanation quality

The calibration methodology follows an evidence-driven process:

Observation
↓
Hypothesis
↓
Adjustment
↓
Evaluation
↓
Decision

Calibration documentation is maintained throughout the repository and serves as the foundation for subsequent experimental evaluation.

Experimental Roadmap

The project currently consists of three major experimental studies.

Experiment 1 – Safe vs Vulnerable Classification

Evaluate the framework's ability to classify secure and vulnerable implementations across a SecurityEval-derived dataset spanning multiple CWE categories.

Primary evaluation metrics include:

Classification accuracy
False positives
False negatives
Confidence
Retrieval quality
Latency
Fix quality
Experiment 2 – Comparative Evaluation

Compare the proposed framework against:

Bandit
CodeQL
Published secure-code-agent methodologies

The goal is to investigate how different analysis paradigms behave across syntax-oriented, semantic, contextual, authorization-related, and workflow-oriented vulnerability categories.

Experiment 3 – End-to-End Workflow Integration

Evaluate the framework as a security-analysis and remediation component within an AI-assisted secure-code-generation workflow inspired by prior secure-code-agent research.

The experiment investigates how contextual retrieval, validation, explanation, and remediation contribute to overall workflow security outcomes.

Dataset

The experimental dataset is derived from SecurityEval methodology and expanded to support:

Vulnerable implementations
Secure implementations
Ground-truth vulnerability labels
Security context profiles
Expanded CWE coverage

The dataset is designed to support reproducibility, broad vulnerability coverage, contextual evaluation, and comparison across multiple analysis approaches.

Dataset documentation is available throughout the repository.

Current Development Focus

Current development activities include:

SecurityEval-derived dataset creation
Security context profile generation
Calibration execution
Hybrid retrieval refinement
Validation methodology documentation
Model configuration evaluation
Expanded CWE coverage
Experimental execution
Comparative evaluation
End-to-end workflow integration
Future Directions

Future research directions include:

Evaluation on larger real-world software systems
Expanded code-aware retrieval techniques
Relationship-aware and graph-based security retrieval
Multi-language vulnerability analysis
Adaptive context engineering
Human-in-the-loop security review workflows
Production development pipeline integration
Specialized security-oriented model adaptation
Reproducibility

The repository documents:

Dataset generation methodology
Calibration procedures
Experimental protocols
Evaluation metrics
Tool configurations
Software versions
Design decisions

The objective is to support transparency, reproducibility, and long-term project evolution.

Repository Structure
docs/
calibration/
experiments/
results/
datasets/
reports/
references/
appendix/
archive/

Each directory contains documentation describing its purpose and relationship to the overall research workflow.

References

Project references, supporting literature, benchmark sources, and related research materials are maintained in the references/ directory.

Key references include literature on:

AI-generated code security
Secure code agents
Retrieval-augmented generation
Common Weakness Enumeration (CWE)
Common Vulnerabilities and Exposures (CVE)
LangGraph orchestration workflows
Static-analysis systems
Disclaimer

This repository documents an active research effort. Methodology, datasets, calibration findings, experimental results, and architectural decisions may evolve as additional evaluation and refinement are completed.

I would be comfortable building the rest of the repository around this README because it now aligns with the planned calibration stage, the expanded SecurityEval evaluation, the comparison experiments, and the end-to-end integration experiment while maintaining the professional, collaborative, and evidence-oriented tone you were aiming for.

Perfect. Now, what would be the next document? Thanks.

The next document should be:

docs/project_overview.md

Not the architecture document.

Not the calibration document.

Not the experiment document.

The Project Overview.

Why This Should Be
Could you generate this document, please? Thank you.

Absolutely. And I think this document is actually one of the most important documents in the entire repository.

The README is the front door.

The Project Overview is the executive summary.

When a professor, researcher, collaborator, department chair, conference reviewer, or future employer wants to quickly understand the project, this is the document they should read.

Unlike the README, which introduces the repository itself, the Project Overview focuses entirely on the research project.

I would recommend the following version:

Project Overview
Project Title

AI-Assisted Vulnerability Detection in LLM-Generated Code: A LangGraph-Orchestrated Workflow for Context-Aware Vulnerability Detection and Secure Code Fixing

Project Summary

Artificial intelligence has become an increasingly important component of modern software development. Large language models can generate functional source code, accelerate prototyping, and assist developers throughout the software engineering lifecycle. However, recent research has demonstrated that AI-generated code may contain security vulnerabilities, including weaknesses that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, and business logic.

Traditional static-analysis systems such as Bandit and CodeQL remain highly effective for many vulnerability categories. However, some vulnerabilities require deeper contextual reasoning regarding intended application behavior, protected resources, authorization expectations, and operational security requirements.

This project investigates whether orchestration-oriented workflows can improve vulnerability analysis of AI-generated software by combining contextual grounding, retrieval-augmented security knowledge, large language model reasoning, repeated validation, remediation generation, and structured reporting within a unified LangGraph-based framework.

The project explores how these components contribute to vulnerability detection, explainability, reliability, and integration within secure software development workflows.

Problem Statement

AI-generated code can contain security vulnerabilities that are difficult to identify using traditional vulnerability-detection approaches alone.

Many modern vulnerabilities involve:

Authorization misuse
Broken access control
Workflow-level security failures
Insecure operational assumptions
Missing security processes
Context-dependent business logic
Dependency and configuration risks

Traditional static-analysis systems excel at identifying many syntax-oriented and semantic vulnerability patterns. However, contextual vulnerabilities often require understanding intended application behavior, security expectations, protected resources, user roles, and operational constraints.

At the same time, large language models provide promising contextual reasoning capabilities but introduce challenges involving:

Hallucinations
Output variability
Prompt sensitivity
Weak reproducibility
Inconsistent explanations

This project investigates whether structured orchestration can help address some of these limitations.

Research Motivation

Recent research has shown that large language models can generate vulnerable software and may struggle to consistently identify or repair security weaknesses within generated code.

These findings raise important questions regarding the role of contextual reasoning, retrieval augmentation, validation strategies, and workflow orchestration in improving AI-assisted vulnerability analysis.

Rather than treating vulnerability detection as a single inference task, this project explores whether a coordinated multi-stage workflow can improve reliability, explainability, and contextual understanding.

The project is motivated by the belief that future advances in AI-assisted security analysis may depend not only on stronger language models, but also on better orchestration, contextual grounding, retrieval quality, validation strategies, and workflow design.

Research Questions

The project investigates four primary research questions.

RQ1 – Architectural Calibration and Evolution

How do orchestration-oriented architectural components—including contextual grounding, retrieval augmentation, prompt engineering, and validation strategies—evolve through calibration, and how do they contribute to the effectiveness of LLM-based vulnerability analysis?

RQ2 – Contextual Vulnerability Reasoning

To what extent can the proposed framework identify vulnerabilities that depend on contextual interpretation, authorization behavior, workflow semantics, operational assumptions, or business logic?

RQ3 – Comparative Detection Performance

How does the proposed framework compare with traditional static-analysis tools and prior secure-code-agent methodologies across diverse vulnerability categories?

RQ4 – End-to-End Workflow Integration

How does integrating the proposed framework into an AI-assisted secure-code-generation workflow influence vulnerability detection, remediation quality, and overall security outcomes?

High-Level Framework

The proposed framework follows a multi-stage orchestration workflow:

Input
↓
Preprocessing
↓
Security Knowledge Retrieval
↓
LLM Vulnerability Detection
↓
Validation
↓
Fix Generation
↓
Structured Reporting

The workflow combines source code, contextual security information, external vulnerability knowledge, vulnerability reasoning, validation mechanisms, remediation generation, and explainable reporting into a unified analysis process.

The architecture is intentionally modular and designed to support future experimentation involving retrieval refinement, model comparisons, expanded datasets, and workflow integration studies.

Current Development Phase

The project is currently focused on:

SecurityEval-derived dataset construction
Security context profile generation
Architectural calibration
Hybrid retrieval refinement
Prompt engineering improvements
Validation methodology documentation
Expanded CWE coverage
Comparative evaluation planning
End-to-end workflow integration preparation

These activities are intended to strengthen the framework before executing expanded experimental studies.

Experimental Roadmap

The project currently includes three major experimental studies.

Experiment 1 – Safe vs Vulnerable Classification

Evaluate vulnerability classification performance across a SecurityEval-derived dataset spanning broad CWE coverage.

Primary metrics include:

Accuracy
False positives
False negatives
Confidence
Retrieval quality
Latency
Remediation quality
Experiment 2 – Comparative Evaluation

Compare the proposed framework against:

Bandit
CodeQL
Prior secure-code-agent methodologies

The objective is to identify strengths, limitations, and areas where contextual reasoning provides additional value.

Experiment 3 – End-to-End Workflow Integration

Evaluate the framework within a secure code-generation workflow inspired by prior secure-code-agent research.

This experiment investigates how contextual retrieval, validation, explainability, and remediation influence overall workflow security outcomes.

Expected Contributions

This project aims to contribute:

A context-aware vulnerability-analysis framework for AI-generated software
A structured orchestration approach combining retrieval, reasoning, validation, and remediation
Insights regarding contextual vulnerability detection
Experimental evaluation across expanded CWE coverage
Comparative analysis against established security-analysis tools
Investigation of end-to-end workflow integration
Documentation of architectural calibration and evolution

The project additionally explores how orchestration-oriented design decisions influence the effectiveness, explainability, and reliability of AI-assisted vulnerability analysis.

Future Directions

Potential future research directions include:

Evaluation on larger real-world software systems
Graph-based and relationship-aware security retrieval
Code-aware retrieval techniques
Multi-language vulnerability analysis
Human-in-the-loop security review workflows
Production software-development integration
Specialized security-oriented model adaptation
Expanded contextual vulnerability benchmarks
Repository Relationship

This document provides a high-level overview of the project.

Additional details can be found throughout the repository:

Calibration documentation → calibration/
Experimental methodology → experiments/
Dataset documentation → datasets/
Results and figures → results/
References and supporting literature → references/
Research reports and presentations → reports/

I would consider this document the "north star" of the repository. Nearly every other document—architecture summaries, calibration plans, experiment plans, roadmap updates, and even future versions of the paper—should remain consistent with the story established here.

Perfect. What would be the next document? Thanks.

The next document should be:

docs/architecture_summary.md

And I would strongly recommend doing this before:

calibration documents
experiment documents
decision log
changelog
Why Architecture Summary Should Come Next

Think about the repository hierarchy:

README

Answers:

What is this repository?

Project Overview

Answers:

What is this project and why does it exist?

Architecture Summary

Answers:

How does the framework work at a high level?

Only after people understand:

The repository
The project
The architecture

does it make sense to show:

calibration
experiments
results

This mirrors the structure we're moving toward in the revised paper:

Introduction
↓
Background
↓
Research Questions
↓
Architecture
↓
Calibration
↓
Experiments
↓
Results
↓
Discussion
↓
Future Work
Why This Document Is Important For Your Project

Your architecture is actually one of the most distinctive parts of the work.

Not because:

LangGraph

by itself is novel.

But because the architecture combines:

contextual security information
retrieval augmentation
vulnerability reasoning
repeated validation
remediation generation
structured reporting

into a coordinated workflow.

The architecture summary becomes the document that explains:

Why these components exist.

before the calibration documents explain:

How they evolved.

What This Document Should NOT Do

I would avoid:

Exact prompts

No.

Internal code

No.

Private implementation details

No.

LangGraph implementation logic

No.

Proprietary workflow specifics

No.

Those belong elsewhere.

What This Document SHOULD Do

Explain:

Purpose

Why the framework exists.

Design Philosophy

Why orchestration is being explored.

Pipeline Overview

High-level workflow.

Component Descriptions

Input

Preprocessing

Retrieval

Detection

Validation

Fix Generation

Reporting

Architectural Principles

Contextual grounding

Retrieval augmentation

Validation

Explainability

Modularity

Evolution Direction

Future improvements:

hybrid retrieval
graph retrieval
expanded context engineering
model flexibility
Why I Think This Is The Best Next Document

After that document exists:

README
✓

Project Overview
✓

Architecture Summary
✓

you have established the foundation of the repository.

Only then would I move into:

calibration/README.md

because calibration is essentially:

How and why the architecture evolved.

And calibration makes much more sense once the architecture itself has been clearly described.

So my recommended order would be:

Completed
README
Project Overview
Next
Architecture Summary
Then
Calibration README
Then
Experimental Methodology
Then
Decision Log
Then
Changelog

That sequence creates a repository that tells a coherent story from motivation → architecture → refinement → evaluation → results, which is exactly the narrative your revised report is aiming to present.

Perfect. Let's create the architecture summary document, please. Also, when you said the evolution direction, the future improvements, remember that we are gonna be having that completed, so it's not really like the future improvements. Or I guess, I don't know, I feel like those future improvements are gonna be things that are implemented once I share this report. So just a sign so you remember. Anyhow, let's go ahead and create the architecture summary documents, please. Thanks.

I agree with your observation.

For this repository, the Architecture Summary should describe:

the architecture as it exists conceptually,
the design philosophy behind it,
the role of each component,
and the architectural directions currently being investigated through calibration and experimentation.

It should not say:

Future improvement: Hybrid retrieval

because, as you pointed out, hybrid retrieval, context engineering, model comparisons, validation refinement, and SecurityEval expansion are part of the current research plan.

Instead, we can describe those as:

Current architectural investigation areas

or

Ongoing architectural refinement areas

which better reflects the project's actual stage.

I would recommend the following document.

Architecture Summary
Purpose

This document provides a high-level overview of the architecture used throughout the project AI-Assisted Vulnerability Detection in LLM-Generated Code: A LangGraph-Orchestrated Workflow for Context-Aware Vulnerability Detection and Secure Code Fixing.

The framework investigates how orchestration-oriented workflows can improve vulnerability analysis of AI-generated software through contextual grounding, retrieval-augmented security knowledge, large language model reasoning, validation strategies, remediation generation, and structured reporting.

The objective is not to replace traditional security-analysis tools. Rather, the framework explores whether coordinated contextual reasoning workflows can provide additional value for vulnerability categories that depend on authorization behavior, workflow semantics, operational assumptions, business logic, and other forms of contextual interpretation.

Architectural Philosophy

The architecture is based on a simple principle:

Better context, better security knowledge, better validation, and better workflow coordination can improve vulnerability-analysis reliability.

Rather than treating vulnerability detection as a single inference task, the framework organizes analysis into multiple stages that contribute different forms of information and reasoning.

The design emphasizes:

Contextual grounding
Retrieval-augmented reasoning
Explainability
Validation consistency
Modular experimentation
Workflow transparency

This philosophy guides both the current implementation and the ongoing calibration and evaluation efforts.

High-Level Workflow

The framework follows a multi-stage orchestration pipeline:

Input
↓
Preprocessing
↓
Security Knowledge Retrieval
↓
LLM Vulnerability Detection
↓
Validation
↓
Fix Generation
↓
Structured Reporting

Each stage contributes a specific function within the overall vulnerability-analysis workflow.

Architectural Components
Input Layer

The workflow begins with source code and associated contextual security information.

In addition to the code itself, the framework supports structured contextual information describing factors such as:

Application purpose
Protected resources
User roles
Authorization requirements
Security expectations
Threat concerns
Operational assumptions
Deployment considerations

The inclusion of context is motivated by the observation that many vulnerabilities cannot be accurately interpreted through source code alone.

For example, vulnerabilities involving access control, workflow behavior, authorization misuse, insecure operational assumptions, or missing security processes often depend on understanding intended application behavior.

Preprocessing Layer

The preprocessing stage prepares incoming information for downstream analysis.

Responsibilities include:

Context normalization
Input formatting
Structured context representation
Workflow state preparation

Although preprocessing does not perform vulnerability analysis directly, it improves consistency throughout the pipeline and reduces variability in downstream reasoning stages.

Security Knowledge Retrieval Layer

The retrieval layer introduces external security knowledge into the analysis process.

The retrieval process is designed to provide contextual grounding through vulnerability-related information derived from sources such as:

Common Weakness Enumeration (CWE)
Common Vulnerabilities and Exposures (CVE)
Vulnerability descriptions
Mitigation guidance
Security terminology
Related weakness relationships

The purpose of retrieval is to support vulnerability reasoning with established security knowledge rather than relying solely on model memory.

Retrieval quality is considered one of the most important factors influencing contextual vulnerability analysis.

Vulnerability Detection Layer

The detection stage performs the primary vulnerability-analysis task.

This stage combines:

Source code
Security context
Retrieved security knowledge

to evaluate whether security weaknesses may be present.

The detector is designed to reason about:

Vulnerability indicators
Authorization behavior
Workflow intent
Business logic
Security assumptions
Operational context

The framework focuses particularly on vulnerabilities that require contextual interpretation beyond recognizable syntax-level patterns.

Validation Layer

The validation stage addresses one of the central challenges associated with large language models: output variability.

Rather than relying on a single analysis result, the framework applies repeated evaluation and aggregation strategies to improve consistency.

The validation process seeks to:

Reduce unstable classifications
Improve confidence estimation
Increase reasoning consistency
Improve trustworthiness of findings

Validation is treated as an architectural component rather than a post-processing step because it directly influences reliability.

Fix Generation Layer

When vulnerabilities are identified, the framework generates remediation guidance and secure-code recommendations.

The remediation stage uses:

Detection findings
Contextual information
Retrieved security knowledge
Mitigation guidance

to produce actionable security recommendations.

In addition to suggesting fixes, this stage contributes to explainability by connecting identified vulnerabilities with appropriate remediation strategies.

Reporting Layer

The final stage generates structured vulnerability-analysis outputs.

Reports may include:

Classification outcomes
Vulnerability mappings
Confidence indicators
Supporting reasoning
Retrieved evidence
Remediation guidance

The reporting stage supports explainability, evaluation, auditing, and comparison with alternative analysis approaches.

Architectural Principles

The framework is guided by several core architectural principles.

Contextual Grounding

Security analysis should consider the operational context surrounding software behavior rather than relying exclusively on source code patterns.

Retrieval-Augmented Reasoning

External security knowledge can improve vulnerability interpretation and strengthen contextual understanding.

Validation-Oriented Analysis

Repeated evaluation and aggregation can improve stability and reduce probabilistic variability.

Explainability

Security findings should be accompanied by reasoning, evidence, and remediation guidance whenever possible.

Modularity

Architectural components should remain separable and independently improvable.

This allows retrieval, validation, prompting, remediation, and contextual-engineering strategies to evolve through experimentation.

Current Architectural Investigation Areas

Several architectural areas are currently being investigated through calibration and experimentation.

These include:

Security context engineering
Structured context representation
Hybrid retrieval strategies
Retrieval reranking approaches
Prompt refinement
Validation methodology optimization
Model allocation strategies
Expanded CWE coverage
SecurityEval-based evaluation
End-to-end workflow integration

These investigations are intended to strengthen contextual reasoning, retrieval quality, explainability, and evaluation rigor.

Architectural Scope

The framework should be viewed as an orchestration-oriented research platform rather than a production-ready security product.

The primary purpose of the architecture is to investigate how contextual grounding, retrieval augmentation, validation strategies, and workflow orchestration influence vulnerability-analysis performance and reliability.

The architecture is therefore designed to support experimentation, evaluation, refinement, and comparative analysis across multiple security-analysis scenarios.

Relationship to the Research Questions

The architecture directly supports the four research questions guiding the project.

RQ1 – Architectural Calibration and Evolution

Investigates how architectural components evolve through calibration and refinement.

RQ2 – Contextual Vulnerability Reasoning

Evaluates the framework's ability to reason about context-dependent vulnerabilities.

RQ3 – Comparative Detection Performance

Supports comparison against traditional static-analysis tools and prior methodologies.

RQ4 – End-to-End Workflow Integration

Examines the role of the framework within broader AI-assisted secure-development workflows.

Summary

The proposed framework combines contextual security information, retrieval-augmented security knowledge, vulnerability reasoning, validation strategies, remediation generation, and structured reporting within a unified orchestration workflow.

The architecture is designed to support systematic experimentation into how workflow coordination, contextual grounding, retrieval quality, and validation mechanisms influence the effectiveness, explainability, and reliability of AI-assisted vulnerability analysis.

I think this version strikes the right balance between:

professional research tone,
consistency with your report,
alignment with the calibration and experiment plans,
protection of implementation details without sounding defensive,
and usefulness as a supporting document for future versions of the paper.
Perfect. Next document, please. Thank you.

The next document should be:

calibration/README.md

And I think this is where your repository starts becoming genuinely interesting.

Up to this point we have created:

✅ README

✅ Project Overview

✅ Architecture Summary

Those explain:

what the project is
why it exists
how it works

The calibration documentation explains something much more important:

Why the architecture ended up looking the way it does.

Why Calibration Comes Next

Remember the revised research narrative:

Problem
↓
Architecture
↓
Calibration
↓
Experiments
↓
Results
↓
Conclusions

The calibration section is the bridge between:

Architecture

and

Experiments

Without calibration, a reviewer sees:

Here is my architecture.

Here are my results.

And naturally asks:

Why did you design it this way?

Calibration answers that question.

Why This Document Matters For Your Project Specifically

Most undergraduate projects have:

Architecture
↓
Experiment
↓
Result

Very few document:

Observation
↓
Hypothesis
↓
Adjustment
↓
Evaluation
↓
Decision

But that process is exactly what your professor has been pushing you toward through:

repeated runs
validation
experimentation
RAG refinement
architecture refinement
context engineering

The calibration documentation becomes evidence that decisions were made systematically rather than arbitrarily.

What This Document Should Accomplish

When somebody reads it they should understand:

Why calibration exists
What was calibrated
How calibration was performed
What decisions calibration influenced
How calibration connects to RQ1

Remember:

RQ1 is now:

How do orchestration-oriented architectural components evolve through calibration and contribute to vulnerability-analysis effectiveness?

The calibration documentation essentially becomes the answer to RQ1.

Recommended Structure

I would create:

calibration/
│
├── README.md
│
├── rag/
│
├── context/
│
├── validation/
│
├── prompts/
│
└── llm_selection/

The README explains the overall calibration methodology.

Then each subfolder contains individual calibration studies.

What Comes After Calibration README

Once calibration README exists, I would create:

docs/experimental_methodology.md

Because then the repository narrative becomes:

README
↓
Project Overview
↓
Architecture Summary
↓
Calibration Methodology
↓
Experimental Methodology

Which mirrors the eventual paper structure almost perfectly.

So my recommendation is:

Next Document

calibration/README.md

After That

docs/experimental_methodology.md

After That

experiments/README.md

Then

decision_log.md

Then

CHANGELOG.md

At that point the repository foundation will be essentially complete, and you'll be ready to start filling it with actual calibration records, dataset information, experiment results, and future report materials.

Perfect. Let's create the next document, the calibration readme, please. Thank you.

Excellent. This is actually one of the most important documents in the repository because it establishes the scientific rigor behind the project.

The README answers:

What is this project?

The Architecture Summary answers:

How does it work?

The Calibration README answers:

Why was it designed this way?

This document should directly support RQ1 – Architectural Calibration and Evolution and become the central location where future calibration records are organized and interpreted.

I would recommend the following version:

Calibration Methodology
Overview

This directory documents the calibration activities conducted throughout the development of the AI-Assisted Vulnerability Detection in LLM-Generated Code framework.

The purpose of calibration is to systematically evaluate and refine architectural components before large-scale experimental evaluation. Rather than treating architectural decisions as fixed assumptions, the project adopts an iterative evidence-driven process in which observations, hypotheses, adjustments, and evaluation outcomes guide architectural evolution.

Calibration serves two primary purposes:

Improve the effectiveness, consistency, and explainability of vulnerability analysis.
Provide empirical justification for architectural decisions investigated throughout the project.

The calibration process directly supports RQ1 – Architectural Calibration and Evolution, which investigates how orchestration-oriented components contribute to the effectiveness of LLM-based vulnerability analysis.

Calibration Philosophy

The framework is based on the principle that vulnerability-analysis performance depends not only on model capability, but also on the quality of contextual information, retrieval mechanisms, validation strategies, workflow design, and architectural coordination.

As a result, architectural components are continuously evaluated and refined prior to expanded experimentation.

Calibration therefore focuses on understanding:

Which architectural components contribute meaningful value
Which configurations improve reliability
Which design choices reduce instability
Which modifications improve contextual reasoning
Which adjustments improve explainability and remediation quality

The objective is not to optimize for a single benchmark result, but rather to improve the overall robustness and transparency of the framework.

Calibration Process

All calibration activities follow the same evidence-driven methodology:

Observation
↓
Hypothesis
↓
Adjustment
↓
Evaluation
↓
Decision
Observation

A limitation, inconsistency, weakness, or opportunity for improvement is identified.

Examples include:

Incorrect vulnerability classifications
Irrelevant retrieval results
Excessive false positives
Inconsistent reasoning
Weak remediation suggestions
Context interpretation failures
Hypothesis

A possible explanation for the observed behavior is proposed.

Examples include:

Missing contextual information
Insufficient retrieval quality
Prompt ambiguity
Validation instability
Incomplete security knowledge
Adjustment

A targeted architectural or configuration modification is introduced.

Examples include:

Context engineering changes
Retrieval strategy modifications
Validation adjustments
Prompt refinements
Model configuration updates
Evaluation

The modified configuration is tested and compared against previous behavior.

Evaluation may include:

Accuracy measurements
Consistency analysis
Retrieval relevance
Explanation quality
Remediation quality
Latency observations
Decision

The results are reviewed and documented.

Potential outcomes include:

Adopt modification
Reject modification
Require additional investigation
Integrate into future experiments
Calibration Categories

Calibration activities are organized into several architectural categories.

Context Engineering Calibration

Directory:

calibration/context/

Purpose:

Evaluate how contextual information influences vulnerability detection, reasoning quality, remediation generation, and explainability.

Examples:

Code-only analysis
Code plus security context
Expanded authorization context
Workflow-oriented context descriptions
Operational security assumptions

Questions investigated:

How much context is necessary?
Which contextual attributes are most valuable?
Does additional context reduce false positives?
Does context improve vulnerability reasoning?
Retrieval Calibration

Directory:

calibration/rag/

Purpose:

Evaluate how external security knowledge contributes to vulnerability analysis.

Areas of investigation include:

CWE retrieval
CVE retrieval
Hybrid retrieval strategies
Retrieval ranking
Context-aware retrieval
Knowledge relevance

Questions investigated:

Does retrieval improve reasoning quality?
Which retrieval strategies provide the most relevant information?
How does retrieval influence explainability?
How does retrieval affect vulnerability coverage?
Validation Calibration

Directory:

calibration/validation/

Purpose:

Investigate strategies for reducing instability associated with probabilistic model outputs.

Areas of investigation include:

Repeated evaluations
Aggregation strategies
Confidence estimation
Consistency measurements

Questions investigated:

How many validation runs are appropriate?
Does aggregation improve stability?
How does validation influence reliability?
What trade-offs exist between consistency and execution cost?
Prompt Calibration

Directory:

calibration/prompts/

Purpose:

Evaluate how prompt design influences vulnerability detection behavior and explanation quality.

Areas of investigation include:

Output structure
Vulnerability reasoning
Explanation formatting
Remediation guidance
Context integration

Questions investigated:

Which prompt structures improve consistency?
Which prompts improve explainability?
How sensitive are results to prompt modifications?
Model Configuration Calibration

Directory:

calibration/llm_selection/

Purpose:

Investigate how model selection and configuration influence analysis outcomes.

Areas of investigation include:

Model comparisons
Configuration comparisons
Multi-model workflows
Performance trade-offs

Questions investigated:

How do different models perform on vulnerability analysis tasks?
What trade-offs exist between quality, latency, and consistency?
Which configurations best support the architectural goals of the framework?
Relationship to Experimental Evaluation

Calibration is conducted prior to expanded experimentation.

The purpose of calibration is not to generate final research conclusions, but rather to improve the quality and justification of the architectural configuration used during formal evaluation.

Insights obtained through calibration inform:

Experimental design
Dataset construction
Retrieval configuration
Validation strategy
Model selection
Reporting methodology

As a result, calibration serves as the foundation for all subsequent experiments.

Documentation Standards

Each calibration record should include:

Calibration Identifier

Unique identifier for traceability.

Example:

CAL-RAG-001
Objective

What is being investigated?

Observation

What motivated the calibration?

Hypothesis

What explanation is being tested?

Adjustment

What change was introduced?

Evaluation Method

How was the adjustment evaluated?

Results

What outcomes were observed?

Decision

What conclusions were reached?

Impact on Architecture

How did the calibration influence architectural evolution?

Connection to Research Question 1

The calibration activities documented in this directory collectively support:

RQ1 – Architectural Calibration and Evolution

How do orchestration-oriented architectural components—including contextual grounding, retrieval augmentation, prompt engineering, and validation strategies—evolve through calibration, and how do they contribute to the effectiveness of LLM-based vulnerability analysis?

The results of these calibration studies provide empirical evidence supporting architectural decisions and establish the foundation for the formal experimental evaluation documented elsewhere in the repository.

Summary

Calibration is treated as a first-class component of the research methodology.

Rather than assuming architectural decisions are correct from the outset, the project adopts a systematic process of observation, hypothesis formation, adjustment, evaluation, and decision-making.

This approach enables architectural evolution to be documented, justified, and connected directly to the research objectives guiding the project
