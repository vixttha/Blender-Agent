"""Primary-source links and tradeoffs for the portable component comparison."""

PROFILES = {
    "Python": ("https://docs.python.org/3/tutorial/", "A standard library and an existing Python codebase can cover scripting, CLIs and services without another toolchain.", "Deployments need a compatible interpreter and dependency environment. Measure CPU-heavy work on the target workload."),
    "JavaScript": ("https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Introduction", "Runs in web browsers and can share code with JavaScript tooling.", "Plain JavaScript needs separate checks or annotations to catch type errors before execution."),
    "TypeScript": ("https://www.typescriptlang.org/docs/handbook/intro.html", "Checks JavaScript contracts statically and fits existing JavaScript tooling.", "Adds a type-checking and build configuration surface. Runtime boundary validation still matters."),
    "Go": ("https://go.dev/ref/mod", "A compiled toolchain and module manifests fit standalone command-line tools and services.", "A second toolchain adds build and release work. Existing host integrations may need adapters."),
    "Rust": ("https://doc.rust-lang.org/cargo/reference/manifest.html", "Cargo provides a standard build and package workflow for native tools and libraries.", "Native interop adds ABI, packaging and platform testing work. End-to-end speedup depends on the measured workload."),
    "C++": ("https://cmake.org/cmake/help/latest/guide/tutorial/index.html", "Can integrate existing native libraries through a compiled toolchain.", "Native builds, memory ownership and platform-specific distribution add maintenance."),
    "Cython": ("https://docs.cython.org/en/latest/src/quickstart/overview.html", "Can compile a narrow Python-compatible kernel with optional static types.", "Adds compiled artifacts and platform-specific distribution. Profile before adopting."),
    "C#": ("https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/", "Fits projects already using .NET libraries and tooling.", "Introducing .NET adds another runtime or publishing surface where the project does not use it."),
    "Java": ("https://docs.oracle.com/javase/specs/", "Fits an existing JVM build and library ecosystem.", "A new JVM distribution and process boundary carry deployment and integration costs."),
    "Kotlin": ("https://kotlinlang.org/docs/java-interop.html", "JVM interoperability can preserve an existing Java ecosystem.", "Adding a second JVM language still changes compilation and maintenance."),
    "Swift": ("https://www.swift.org/documentation/", "Fits Swift toolchains and native Apple-platform integrations.", "Cross-platform package, UI and host support need separate verification."),
    "Ruby": ("https://www.ruby-lang.org/en/documentation/", "Fits an already established Ruby runtime and libraries.", "Adds interpreter and dependency maintenance when the project uses a different ecosystem."),
    "PHP": ("https://www.php.net/manual/en/intro-whatis.php", "Fits an existing PHP web runtime.", "A new runtime and dependency stack need a maintained deployment path."),
}

BLENDER_API = "https://docs.blender.org/api/4.5/info_overview.html"

# Alternatives are screened against each job. Inventory works with languages
# outside this catalog, for which the report records the missing comparison.
ROLES = {
    "blender-worker": ("Blender in-process work", ("Python", "C++")),
    "browser": ("Browser application", ("TypeScript", "JavaScript")),
    "javascript": ("JavaScript-runtime package", ("TypeScript", "JavaScript")),
    "cli": ("Command-line tooling", ("Python", "Go", "Rust", "TypeScript", "JavaScript")),
    "service": ("Service or protocol adapter", ("Python", "TypeScript", "JavaScript", "Go", "C#",
                                               "Java", "Kotlin", "Ruby", "PHP")),
    "native": ("Native library or measured CPU kernel", ("Rust", "C++", "Cython")),
    "jvm": ("JVM component", ("Java", "Kotlin")),
    "dotnet": (".NET component", ("C#",)),
    "swift": ("Swift component", ("Swift",)),
    "go": ("Go component", ("Go",)),
    "python": ("Python package", ("Python",)),
    "ruby": ("Ruby component", ("Ruby",)),
    "php": ("PHP component", ("PHP",)),
    "unknown": ("Unclassified source", ()),
}
