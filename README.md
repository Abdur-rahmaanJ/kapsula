<div align=center width=150>

  ![](https://raw.githubusercontent.com/Abdur-rahmaanJ/kapsula/stable/assets/logo.png)
  
</div>

# kapsula

>  "In 2025 the docs should be a single your_project.md text file that is intended to go into the context window of an LLM."
> 
> -- Andrej Karpathy

Great for adding markdown docs to llm.

Dead simple docs generator. Generates html and markdown docs. 

Have a clear view of the codebase without knowing any tooling

```
kapsula . # path to folder
kapsula path/ --exclude venv another_folder # excludes folders, venv excluded by default
kapsula /path --debug # debug
kapsula [directories] [output.html] [output.md] [flags]
kapsula scripts buns docs.html docs.md --exclude venv
```

Makes onboarding a breeze!


## Generated Doc

- Treeview

![](https://raw.githubusercontent.com/Abdur-rahmaanJ/kapsula/stable/assets/tree_view.png)

- List view

![](https://raw.githubusercontent.com/Abdur-rahmaanJ/kapsula/stable/assets/list_view.png)

- Search

![](https://raw.githubusercontent.com/Abdur-rahmaanJ/kapsula/stable/assets/search.png)
