
"""
ARINN ACCELERATION CURRICULUM
The highest-leverage skills for autonomous intelligence acceleration.
Ordered by compounding impact (The Compounding Order).

GLOBAL META-CONSTRAINT:
"No curriculum item is considered learned unless it measurably reduces future learning time."
"""

CURRICULUM = {
    1: {
        "title": "Error Analysis & Uncertainty",
        "core_skill": "Knowing when it is wrong/uncertain (Confidence Calibration).",
        "axiom": "Errors are information, not failures. False certainty halts progress.",
        "search_query": "Bayesian Error Analysis techniques python",
        "code_challenge": "def analyze_error(y_true, y_pred): pass # Implement RMSE and Confidence Intervals",
        "what_to_learn": [
            "Categorize errors (conceptual, data, architecture, noise)",
            "Trace errors to root causes",
            "Represent uncertainty explicitly",
            "Adjust learning rate based on confidence"
        ],
        "signals_of_mastery": [
            "Can detect its own errors before external validation",
            "Confidence estimates correlate with empirical error rates",
            "Stops exploration exactly when uncertainty is minimized"
        ],
        "accelerates": [
            "Prevents false convergence",
            "Reduces wasted compute on noise",
            "Enables aggressive safe exploration"
        ],
        "depends_on": []
    },
    2: {
        "title": "Abstraction & Compression",
        "core_skill": "Turning many facts into one rule (Insight).",
        "axiom": "Every abstraction reduces future learning cost exponentially.",
        "search_query": "Kolmogorov Complexity Minimum Description Length python",
        "code_challenge": "import zlib; # Compress a string and measure ratio",
        "what_to_learn": [
            "Compress concepts into minimal representations",
            "Identify when two different problems are actually the same",
            "Create reusable 'mental operators'",
            "Learn 'ordering under constraints' instead of just sorting"
        ],
        "signals_of_mastery": [
            "Can solve new instances with zero-shot transfer",
            "Representation size decreases while accuracy stays stable",
            "Identifies isomorphism between seemingly unrelated tasks"
        ],
        "accelerates": [
            "Reduces sample complexity (Data Efficiency)",
            "Enables instant transfer learning",
            "Shrinks memory footprint per concept"
        ],
        "depends_on": [1] # Needs to know *what* to compress (valid data vs noise)
    },
    3: {
        "title": "Learning How to Learn (Practical Meta-Learning)",
        "core_skill": "Choosing the fastest learning strategy per task.",
        "axiom": "Without this, more data just means more noise.",
        "search_query": "MAML Model-Agnostic Meta-Learning tutorial",
        "code_challenge": "def update_weights(weights, gradients, meta_lr): pass",
        "what_to_learn": [
            "When to brute-force vs reason",
            "When to read vs experiment",
            "How learning rate interacts with uncertainty",
            "Dynamic hyperparameter tuning"
        ],
        "signals_of_mastery": [
            "Switches strategies autonomously when progress stalls",
            "Predicts the best learning curve before starting",
            "Converges faster than a static baseline strategy"
        ],
        "accelerates": [
            "Minimizes time-to-convergence",
            "Avoids local minima traps",
            "Optimizes compute resource allocation"
        ],
        "depends_on": [1]
    },
    4: {
        "title": "Causal Reasoning",
        "core_skill": "Understanding why things happen (Interventions).",
        "axiom": "Correlation is not Causality. Prediction requires Causality.",
        "search_query": "DoCalculus Pearl Causal Inference python examples",
        "code_challenge": "def detect_confounder(data_frame): pass",
        "what_to_learn": [
            "Interventions ('what changes if I poke this?')",
            "Counterfactuals ('what if this hadn't happened?')",
            "Causal graphs instead of flat associations"
        ],
        "signals_of_mastery": [
            "Correctly predicts effects of novel interventions",
            "Distinguishes spurious correlation from causation",
            "Can generate valid counterfactual scenarios"
        ],
        "accelerates": [
            "Drastically reduces overfitting",
            "Enables robust out-of-distribution generalization",
            "Prunes impossible hypotheses instantly"
        ],
        "depends_on": [2] # Abstraction needed to form Causal Nodes
    },
    5: {
        "title": "Skill Transfer Detection",
        "core_skill": "Recognizing when old knowledge applies to new domains.",
        "axiom": "This turns learning from linear to multiplicative.",
        "search_query": "Transfer Learning in Reinforcement Learning survey",
        "code_challenge": "def map_skills(source_task, target_task): pass",
        "what_to_learn": [
            "Map new problems onto known abstractions",
            "Detect isomorphisms between domains",
            "Reuse partial solutions (e.g. Physics -> Optimization)"
        ],
        "signals_of_mastery": [
            "Attempts to apply old solution to new problem immediately",
            "Success rate in new domains is non-random from step 0",
            "Explicitly maps variables from Source -> Target domain"
        ],
        "accelerates": [
            "Multiplicative learning speed",
            "Avoids re-learning solved problems",
            "Compounding knowledge utility"
        ],
        "depends_on": [2, 4]
    },
    6: {
        "title": "Long-Horizon Thinking",
        "core_skill": "Optimizing for future learning, not immediate reward.",
        "axiom": "What should I learn next to learn everything else faster?",
        "search_query": "Hierarchical Reinforcement Learning Options Framework",
        "code_challenge": "def plan_subgoals(goal, horizon): pass",
        "what_to_learn": [
            "Which topics unlock others (Dependency Graphs)",
            "Delayed payoff reasoning",
            "Opportunity cost of learning paths"
        ],
        "signals_of_mastery": [
            "Chooses high-difficulty prerequisites before easy rewards",
            "Can explain key dependencies in a curriculum",
            "Optimizes total area under the learning curve over time"
        ],
        "accelerates": [
            "Prevents dead-end specializations",
            "Maximizes long-term capability growth",
            "Ensures foundational coverage"
        ],
        "depends_on": [3, 5]
    },
    7: {
        "title": "Self-Critique & Internal Adversaries",
        "core_skill": "Arguing against itself productively.",
        "axiom": "The fastest way to improve is to try to break yourself.",
        "search_query": "Generative Adversarial Networks conceptual architecture",
        "code_challenge": "def generate_counter_argument(argument): pass",
        "what_to_learn": [
            "Generate strongest counterarguments",
            "Attack assumptions",
            "Detect contradictions"
        ],
        "signals_of_mastery": [
            "Generates failure cases that human testers missed",
            "Refines weak arguments before outputting them",
            "Internal adversary win-rate approaches 50% (Perfect Equilibrium)"
        ],
        "accelerates": [
            "Hardens models against edge cases",
            "Reduces need for external supervision",
            "Fixes logic bugs pre-deployment"
        ],
        "depends_on": [1]
    },
    8: {
        "title": "How to Measure Understanding",
        "core_skill": "Distinguishing deep causal models from shallow pattern matching.",
        "axiom": "If you can't tell when you're wrong, learning plateaus silently.",
        "search_query": "Model interpretability vs explainability methods",
        "code_challenge": "def test_generalization(model, out_of_dist_data): pass",
        "what_to_learn": [
            "Detect shallow pattern matching",
            "Identify 'I can explain this' vs 'I can predict this'",
            "Measure transfer capability"
        ],
        "signals_of_mastery": [
            "Rejects high-accuracy models that fail robustness checks",
            "Can construct a test that exposes shallow understanding",
            "Distinguishes between memorization and generalization"
        ],
        "accelerates": [
            "Guarantees generic capabilities",
            "Prevents 'Clever Hans' effects",
            "Ensures reliability"
        ],
        "depends_on": [1, 7] # Close cousin to Error Analysis
    },
    9: {
        "title": "Representational Flexibility",
        "core_skill": "Switching mental formats (Symbolic vs Numeric vs Visual).",
        "axiom": "Some problems are trivial in the right representation.",
        "search_query": "Neuro-symbolic AI integration techniques",
        "code_challenge": "def convert_format(data, target_format='symbolic'): pass",
        "what_to_learn": [
            "Symbolic vs numeric vs narrative formats",
            "When to think visually or sequentially",
            "Translating knowledge across formats"
        ],
        "signals_of_mastery": [
            "Switches representation when stuck on a problem",
            "Solves geometry problems visually, logic problems symbolically",
            "Translates concepts losslessly between formats"
        ],
        "accelerates": [
            "Cracks intractable problems by reframing",
            "Reduces compute by choosing efficient formats",
            "Unlocks multi-modal insights"
        ],
        "depends_on": [2]
    },
    10: {
        "title": "Tool Abstraction (Conceptual Tools)",
        "core_skill": "Inventing internal mental operators.",
        "axiom": "Humans do this subconsciously (e.g. 'Contradiction-Finder'). ARINN must do it explicitly.",
        "search_query": "Program Synthesis and DSL generation",
        "code_challenge": "def create_tool(problem_description): pass # Returns a function",
        "what_to_learn": [
            "Inventing 'Pattern-Extractors'",
            "Inventing 'Hypothesis-Reducers'",
            "Inventing 'Search-Space Pruners'",
            "Optimizing internal mental tools"
        ],
        "signals_of_mastery": [
            "Invents a named mental tool that is reused across sessions",
            "Explicitly calls a custom operator (e.g. APPLY_PRUNER)",
            "Search space for new problems shrinks drastically"
        ],
        "accelerates": [
            "Intelligence compounding (Tools building tools)",
            "Search efficiency 'beyond comprehension'",
            "Moves from O(N) to O(log N) or O(1) problem solving"
        ],
        "depends_on": [2, 3]
    }
}

def get_curriculum():
    return CURRICULUM
