# CodeGen
For this project I want to use a local LLM model to help generate project templates or to generate boilerplate code for projects. Using the ollama library and functions that allow a LLM model to run code via functions.


After coding some more and trying to get the LLM to do file creation and writing to a file. The LLM would either end up in a infinite loop or just run a incorrect function. And after some thinking I decided to change up the process a little bit.

Similar to how my clint CLI Tool works, I will have user defined templates for projects and then just use LLM for generating the boilerplate code.

Using an LLM it will be able to generate more specific boilerplate code for the given project as apposed to clint having the user write template code in the templates. Also this allows the user to only have the template structure thought out. And leave the code to the LLM.

I'll probably end up using a json to represent the templates and the structure similar to how clint does templates (but without the code, just the structure).

Hopefully, the LLM will be able to tailor the boilerplate code to the project based either on the name of the project or a description of the project that is set in the template.

I have the model generating code and writing to the appropriate file, but the model generates '```' at the beginning and the end of the file. As well as having the language at the top. So for now I just have a list to check what file type it is and then remove the correct language that is put at the top. But for now it works.

