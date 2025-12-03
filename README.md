### OCTOPIE - Machine Learning Anti-Virus Experiment

# 🧬 Digital Immune System: Pathogen-Inspired Cyber Defense Framework  

> From **cells to cyber** — building a smarter, more adaptive antivirus inspired by *you know… the actual human immune system.*

---

## 🧠 What’s This All About?

Traditional antivirus systems? They’re like bouncers who only recognise last week’s troublemakers.  
This project flips that idea — building a **bio-inspired defense system** that learns, adapts, and remembers threats, just like your body does when it fights viruses and bacteria.  

We’re borrowing ideas from immunology and machine learning to create an **adaptive, layered antimalware architecture** that doesn’t just react — it *evolves*.

---

✨ Adaptive Antimalware Framework (PoC)
======================================

This README section outlines the project's conceptual architecture and documents the recent changes implemented to establish a modular, production-ready development environment.

* * * * *

## ⚙️ How It Works
---------------

Mapping the human body defense to a computer. Each layer of this digital immune system plays the role of a biological counterpart:

| **🧩 Biological Function** | **💻 Cybersecurity Role** | **🔬 Implementation Layer** |
|           ---              |            ---            |             ---             |
| **Sensory Receptors**      | Collect system telemetry  | Layer 1: Signal Acquisition |
| **Innate Immunity**        | Heuristic & NSA detection |   Layer 2: Innate Detection |
| **Adaptive Immunity**      |      ML-based analysis    |  ayer 3: Adaptive Detection |
| **Inflammatory Response**  |   Quarantine & rollback   | Layer 4: Response & Containment |
| **Memory Cells**           | Reinforcement & federated learning | Layer 5: Memory & Learning |

* * * * *

## 🧩 The System Architecture (In a Nutshell)
------------------------------------------
The system enforces a strict, unidirectional data pipeline that mirrors biological escalation paths.
```
graph TD
  A [Signal Acquisition Layer] --> B[Innate Detection Layer]
  B --> C[Adaptive Detection Layer]
  C --> D[Response & Containment Layer]
  D --> E[Memory & Learning Layer]
  E --> B
  subgraph "Biological Analogy"
    A1[Sensory Receptors]
    B1[Macrophages / Innate Cells]
    C1[T-Cells / Dendritic Cells]
    D1[Inflammation / Containment]
    E1[Memory Cells]
  end
  A --- A1
  B --- B1
  C --- C1
  D --- D1
  E --- E1
  linkStyle 0,1,2,3,4 stroke:#2962FF,stroke-width:2p

```

* * * * *

## 🛠️ III. Recent Changes and Modularization
------------------------------------------
Structure has been updated for stability, controlled module importing, and strict separation of concerns between layers.

### 1\. Environment and Utility Additions

These files manage dependencies and provide critical shared functionality.

-   **`venv/` (Virtual Environment)**

    -   **Purpose:** Ensures project dependencies (`psutil`, `scikit-learn`, etc.) are isolated from the global system environment-also a working testing environment

-   **`requirements.txt`**

| **Old Version (Problematic)** | **New Recommended Version** | **Reason for Change** |
| --- | --- | --- |
| **`seaborn==0.12.3`** | **`seaborn>=0.13.0`** (or just `seaborn`) | Version **0.12.3** does not have wheels for **Python 3.12**. |
| **`pandas-profiling==5.2.0`** | **`ydata-profiling`** (no version pin) | The `pandas-profiling` project has been **renamed** to `ydata-profiling`. |
| **`tensorflow==2.14.0`** | **`tensorflow>=2.16.1`** (or just `tensorflow`) | Version **2.14.0** does not support **Python 3.12**. |


-   **`setup.py`**

    -   **Purpose:** Defines the project as a package. Allows installation in **Editable Mode** (`pip install -e .`), which is essential for resolving module imports like `from src.utils...`.

-   **`src/utils/telemetry_collectors.py`** (Core Layer 1 Utility)

    -   **Purpose:** **The Data Generator.** Contains the actual code (e.g., `collect_basic_system_metrics`) that interfaces with the OS (`psutil`) to pull raw resource usage data. It forms the backbone of Layer 1.

-   **`src/utils/data_reader.py`** (NEW Utility Module)

    -   **Purpose:** **The Data Bridge.** Contains the `read_telemetry_jsonl` function. This utility is used by Layer 2 to consume data saved by Layer 1, enforcing separation.

### 2\. Layer Code Refactoring

The core change is making Layer 2 entirely dependent on Layer 1's output, removing redundant data collection logic.

#### A. `layer1_signal_acquisition.py` (Layer 1)

-   **Status:** **Stable.** No functional code changes.

-   **Role:** Remains the single **source of truth** for telemetry data, writing raw JSON records to `data/telemetry.jsonl`.

#### B. `layer2_innate_detection.py` (Layer 2)

-   **Functional Change:** The function `collect_baseline` was **REMOVED**.

    -   **Rationale:** Eliminates redundancy. Layer 2 is now purely a data *processor* (ML layer), not a data *collector*.

-   **New Dependency:** Imports `read_telemetry_jsonl` from the new `src/utils/data_reader.py` file.

-   **Revised Training:** The `train_oneclass_svm` function was updated to:

    1.  Call `read_telemetry_jsonl` to load the baseline.

    2.  Process the loaded data for training the One-Class SVM.

-   **Argument Removal:** Command-line arguments (`--samples`, `--interval`) were removed as they are no longer relevant for a processor layer.


### UPDATED REQUIREMENTS FILES

The recent changes were focused on creating a **robust, non-conflicting dependency environment** and strictly enforcing the modular pipeline structure .

1\. Dependency Isolation Strategy 📦
------------------------------------

The monolithic `requirements.in` file was broken down into a layered structure to prevent compatibility issues, particularly between the heavy **Deep Learning stack** and the core data libraries.

| **New File** | **Purpose** | **Key Libraries** | **Rationale** |
| --- | --- | --- | --- |
| **`requirements-base.in`** | **Core Foundation.** Essential libraries for all layers and data manipulation. | `psutil`, `pandas`, `numpy` | Must be installed first. |
| **`requirements-layer1.in`** | **Acquisition Tools.** Required for system profiling and data analysis within Layer 1. | `ydata-profiling` | Isolated due to its large, complex transitive dependency tree. |
| **`requirements-layer2.in`** | **Innate Detection.** Minimal ML dependencies for the One-Class SVM. | `scikit-learn` | Kept light and separate from the deep learning tools. |
| **`requirements-layer3-5.in`** | **Deep Learning Stack.****HEAVY** libraries for Adaptive Detection and Memory/Learning. | `torch`, `tensorflow` | **Crucially isolated** as they cause the most version conflicts with each other and core packages. |

This strategy ensures that during initial development (Layers 1 and 2), you only install necessary, lightweight packages, avoiding hours of dependency resolution conflicts.

2\. Layer 2 Role Clarification 🧱
---------------------------------

The second major change was to the code, reinforcing Layer 2's role as a processor:

-   **`collect_baseline` Function Removed:** Layer 2 no longer generates its own data.

-   **New Utility:** The addition of `src/utils/data_reader.py` (containing `read_telemetry_jsonl`) now forces Layer 2 to **consume** the `data/telemetry.jsonl` file created by Layer 1.

This creates a clean, non-redundant pipeline: **Layer 1 collects data, Layer 2 analyzes that collected data.**