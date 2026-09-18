def classifier_query(query):
    query=query.lower()
    coding_keywords = [
        "code",
        "coding",
        "python",
        "javascript",
        "java",
        "c++",
        "c#",
        "flask",
        "django",
        "react",
        "node",
        "function",
        "class",
        "algorithm",
        "debug",
        "debugging",
        "error",
        "exception",
        "api",
        "database",
        "sql",
        "mongodb",
        "program",
        "programming"
    ]
    reasoning_keywords = [
        "calculate",
        "solve",
        "equation",
        "mathematical",
        "logic",
        "reason",
        "analyze",
        "analysis",
        "compare",
        "derive"
    ]
    if any(word in query for word in coding_keywords):

        task = "coding"

    elif any(word in query for word in reasoning_keywords):

        task = "reasoning"

    else:

        task = "general"

    # -------------------------
    # Complexity
    # -------------------------

    word_count = len(query.split())

    if word_count < 15:

        complexity = "simple"

    elif word_count < 50:

        complexity = "medium"

    else:

        complexity = "complex"

    return {
        "task": task,
        "complexity": complexity
    }
