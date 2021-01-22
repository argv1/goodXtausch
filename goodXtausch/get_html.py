import pandas as pd

def get_html(combined_df, result_f):
    pd.set_option('display.max_colwidth', None)
    combined_df['link'] = "<a href='"+combined_df['url']+"'>"+combined_df['title'].astype(str).str[0:15]+"...</a>"
    html_table = combined_df.to_html(escape=False)
    with open(result_f, "w", encoding="utf-8") as f:
        for line in html_table:
            f.write(line)