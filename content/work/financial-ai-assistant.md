---
{"title":"SS&C Financial AI Assistant","slug":"financial-ai-assistant","category":"Applied AI · Financial workflows","description":"A team capstone bringing conversational search to financial risk information.","tools":["RAG","Chroma DB","Reciprocal rank fusion"],"image":"/assets/retrieval-flow.svg","image_alt":"A question is used to retrieve relevant documents and generate an answer","featured":true,"status":"Team project"}
---
## From scattered information to a conversation

Financial risk analysis often starts with a search: finding the right information across documents, metadata, and lists of risk factors. Our capstone, the Financial Risk Insight Engine, explored a conversational alternative. The goal was to help users ask a question, find relevant material, and read a useful summary in one place.

## My contribution

I worked on the product and retrieval design, including the move from in-memory storage to Chroma DB and iterations on the answer workflow. A central concern was how to make the system useful without letting a plausible-sounding answer drift beyond the information available to it.

This was a team effort with Soham Bidyadhar, Albert Nguyen, Kimberly Simmonds, and Isha Verma.

## The challenge

The project had to address two connected problems: inconsistent source information and answers that could introduce risk factors outside the source material. A conversational interface alone would not solve either. The information behind it needed to be organized, and the answer needed to stay connected to that information.

## How the system works

The project used retrieval-augmented generation (RAG): retrieve relevant information first, then use it to support the answer. Chroma DB provided semantic search over the knowledge base. Reranking and reciprocal rank fusion helped order candidate results, while chat history supported follow-up questions.

![An overview of the question, retrieval, and answer workflow](/assets/retrieval-flow.svg)

The product work focused on how these pieces fit together for a user asking a financial risk question. Retrieval quality, conversation context, and the clarity of the resulting summary all mattered.

## The resulting workflow

The prototype brought conversational questions, document retrieval, and human-readable summaries into a single workflow. It explored how an AI assistant could help users navigate risk information and investigate questions without relying solely on manual searches.

## Lessons and limitations

Relevant retrieval is only part of a reliable answer. A system also needs to recognize when the source material is incomplete and avoid filling those gaps with invented details. Reranking can improve the ordering of results, but it does not guarantee that a generated answer is correct.

The project reinforced the importance of evaluating both the information retrieved and the answer built from it. A useful assistant needs to make its sources and limits understandable to the person using it.
