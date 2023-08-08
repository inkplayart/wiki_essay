# wiki_essay

Searches Wikipedia for articles, then writes an essay about them. 

## Warnings

This starter code is designed to use the openAI API. It uses gpt-3.5 and gpt-4, so if you increase the number of iterations it may cost a lot. You are assuming that responsiblity for yourself!

## Required libraries

This code relies on the requests and openai libraries. Both can be installed via pip or your favorite package manager.

## Getting started

Think of this as starter code. It uses the openAI API and two models: gpt-3.5-turbo (the 4K context version) is used to extract the search terms and Wikipedia summaries. gpt-4 is used to generate the essay itself. If you want to use another model modify the `get_response` function, which is on line 35.

The program begins by searching wikipedia for the term stored in `current_search_term`, defined on line 12. It then proceeds for `num_iterations` iterations - each iteration it generates search terms from the previous wikipedia summary, and finds one it hasn't searched for before. It then searches Wikipedia and gets `num_results` results from the search. It finds a page it hasn't seen before, and extracts its summary to repeat the process.

When it is done, it dumps the raw Wikipedia text into the file defined in `filename`, which must include a "." in it somewhere, and writes an essay to the file `filename.split(".")[0] + "_essay.txt"`. 


