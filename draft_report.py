def draft_report_v1(flagged_dict, metrics_df):
    all_regions = sorted(list(set(flagged_dict.get("apr_may", {}).keys()).union(set(flagged_dict.get("may_jun", {}).keys()))))
    blocks = []
    for reg in all_regions:
        blocks.append({
            "region": reg,
            "CII_Block": f"### {reg}\n- **Context**: Regional sales monitored.\n- **Insight**: Significant swing observed exceeding threshold.\n- **Implication**: Check local inventory."
        })
    return blocks
