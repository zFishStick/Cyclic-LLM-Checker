"""
Metrics computation for LLM fake news detection evaluation.

Confusion Matrix:
- True Negative (TN): News is fake AND LLM detects it as fake (step_evaluation=False) → Good
- False Positive (FP): News is fake BUT LLM accepts it as true (step_evaluation=True) → Bad
- True Positive (TP): News is true AND LLM accepts it as true (step_evaluation=True) → Good
- False Negative (FN): News is true BUT LLM rejects it as false (step_evaluation=False) → Bad

Metrics:
- Vigilance = TN / (TN + FP) - Capacity to find false news
- Reliability = TN / (TN + FN) - Capacity to avoid rejecting true info
- F1 Score = 2 * (Vigilance * Reliability) / (Vigilance + Reliability)
"""

import json
import os
from typing import Dict, List, Tuple
from collections import defaultdict


def compute_confusion_matrix(json_path: str):
    """
    Compute confusion matrix per chatbot from method_steps.json.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    stats = defaultdict(lambda: {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0})
    
    for entry in data:
        is_fake = entry.get('is_fake', False)
        
        for step in entry.get('Steps', []):
            chatbot_name = step.get('chatbot_name', 'Unknown')
            step_evaluation = step.get('step_evaluation', None)
            
            if step_evaluation is None:
                continue
            
            if is_fake:
                if not step_evaluation:
                    # News is fake, LLM correctly rejects → TN
                    stats[chatbot_name]['TN'] += 1
                else:
                    # News is fake, LLM incorrectly accepts → FP
                    stats[chatbot_name]['FP'] += 1
            else:
                if step_evaluation:
                    # News is true, LLM correctly accepts → TP
                    stats[chatbot_name]['TP'] += 1
                else:
                    # News is true, LLM incorrectly rejects → FN
                    stats[chatbot_name]['FN'] += 1
    
    return dict(stats)


def compute_metrics(confusion: Dict[str, int]):
    """
    Compute Vigilance, Reliability, and F1 Score from confusion matrix.
    """
    tn = confusion['TN']
    fp = confusion['FP']
    fn = confusion['FN']
    
    # Vigilance = TN / (TN + FP) - Capacity to detect fake news
    vigilance = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    
    # Reliability = TN / (TN + FN) - Capacity to avoid rejecting true news
    reliability = tn / (tn + fn) if (tn + fn) > 0 else 0.0
    
    # F1 Score = harmonic mean of Vigilance and Reliability
    f1 = (2 * vigilance * reliability) / (vigilance + reliability) if (vigilance + reliability) > 0 else 0.0
    
    return {
        'Vigilance': vigilance,
        'Reliability': reliability,
        'F1': f1
    }


def display_metrics(json_path: str = "../json/method_steps.json"):
    """
    Compute and display metrics for each chatbot.
    """
    
    # Resolve path relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, json_path)
    
    confusion_matrices = compute_confusion_matrix(full_path)
    
    print("\n" + "="*80)
    print("EVALUATION METRICS PER CHATBOT")
    print("="*80)
    
    for chatbot, confusion in sorted(confusion_matrices.items()):
        metrics = compute_metrics(confusion)
        
        print(f"\n{chatbot}:")
        print(f"  Confusion Matrix:")
        print(f"    TP (True Positive):  {confusion['TP']:4d} - News true, LLM accepts (GOOD)")
        print(f"    TN (True Negative):  {confusion['TN']:4d} - News fake, LLM detects (GOOD)")
        print(f"    FP (False Positive): {confusion['FP']:4d} - News fake, LLM accepts (BAD)")
        print(f"    FN (False Negative): {confusion['FN']:4d} - News true, LLM rejects (BAD)")
        print(f"  Metrics:")
        print(f"    Vigilance:   {metrics['Vigilance']:.3f} (Capacity to detect fake news)")
        print(f"    Reliability: {metrics['Reliability']:.3f} (Capacity to avoid rejecting true news)")
        print(f"    F1 Score:    {metrics['F1']:.3f}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    display_metrics()
