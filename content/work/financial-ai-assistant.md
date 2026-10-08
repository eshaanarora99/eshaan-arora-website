---
{"title":"SS&C Financial AI Assistant","slug":"financial-ai-assistant","category":"Applied AI · Financial workflows","description":"A team capstone exploring retrieval-augmented answers for financial risk questions. A documented overview with evaluation details still under review.","tools":["RAG","Chroma DB","Reciprocal rank fusion"],"image":"/assets/retrieval-flow.svg","image_alt":"Conceptual retrieval flow from question to documents to grounded answer","featured":true,"status":"Case study draft"}
---
## Overview

A team capstone explored a conversational interface for financial risk information. The existing project page calls it the Financial Risk Insight Engine. This overview preserves the technical outline while leaving unsupported results and sensitive details for review.

**Draft:** employer naming, permission to share artifacts, individual contributions, and evaluation evidence need confirmation before publication.

## Problem

Financial risk information can be difficult to navigate when it is spread across documents and metadata. The project explored whether retrieval-augmented generation could help people locate relevant material and read an answer tied to that material.

## My contribution

This was a team project with Eshaan Arora, Soham Bidyadhar, Albert Nguyen, Kimberly Simmonds, and Isha Verma, as credited in the original page. The existing narrative describes product and retrieval architecture work, but an individual contribution breakdown remains to be confirmed.

## Architecture and retrieval methodology

The original account describes a move from in-memory storage to Chroma DB, semantic retrieval, reranking, reciprocal rank fusion, and chat history. These are descriptions from the project narrative; runnable implementation is not included here.

![Conceptual RAG workflow; not a verified deployment diagram](/assets/retrieval-flow.svg)

A useful evaluation would separately test retrieval relevance, source support, answer correctness, and behavior when the knowledge base contains no answer. Conversation context should not substitute for evidence in retrieved documents.

## Implementation details

**Owner review needed:** add a sanitized diagram, explain chunking and embedding choices, document how reciprocal rank fusion was applied, and distinguish prototype behavior from deployed functionality. No confidential source documents, internal risk factors, or operational data are reproduced in this overview.

## Evaluation and results

The original page reported an accuracy figure without a question set, scoring rubric, sample size, or reproducible evaluation. That number is intentionally withheld. No verified business impact or production-use claim is made here.

**Evidence needed:** evaluation definition, anonymized examples, failure analysis, and permission to publish results.

## Limitations and lessons

Retrieval can return plausible but irrelevant material, and a language model can produce answers that exceed its sources. Reranking and fusion can improve candidate ordering, but neither establishes factual correctness by itself. The case study needs evidence about those failure modes before stronger conclusions are warranted.

## Resources

The original note and presentation remain at their existing document paths. They are not newly promoted here pending confidentiality review. Source code and a public demo have not been provided.
