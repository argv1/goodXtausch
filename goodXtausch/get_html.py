import pandas as pd
from   pathlib import Path

# Global settings
base_path = Path(__file__).parent.absolute()
result_f = base_path / 'output.html'

def get_html(combined_df):
    pd.set_option('display.max_colwidth', None)
    combined_df['link'] = "<a href='"+combined_df['url']+"'>"+combined_df['title'].astype(str).str[0:15]+"...</a>"
    html_table = combined_df.to_html(escape=False)
    with open(result_f, "w", encoding="utf-8") as f:
        for line in html_table:
            f.write(line)