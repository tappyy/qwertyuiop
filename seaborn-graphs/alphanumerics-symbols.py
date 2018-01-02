import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

# import csv and convert to dataframe
df_pwds = pd.read_csv('output.csv')
df_pwds.sort_values('Crack Time H', inplace=True)

# sizing
sb.set_style('whitegrid')
sb.set_context("notebook")
plt.figure(figsize=(6, 6)) #600 x 600 dim
plt.subplots_adjust(bottom=0.2) # increase bottom margin

# create plot
graph = sb.barplot(x='Password', y='Crack Time H', data=df_pwds, palette=sb.color_palette("RdYlGn", 4))

# annotate bar values
for p in graph.patches:
    height = p.get_height()
    graph.text(p.get_x()+p.get_width()/2.,
            height + 100,
            '{:1.2f}'.format(height),
            ha="center", fontsize=8)

# styling
bars = ('lowercase', 'lowercase\nand digits','lowercase\nand uppercase', 'lowercase\nand symbols')
ypos = np.arange(len(bars))
plt.xticks(ypos, bars) # custom x-axis labels
plt.title('Hours taken to crack 8-letter password')
plt.xlabel('')
plt.ylabel('')
sb.despine(left=True, bottom=True)

# notes
graph.figure.text(0.05, 0.05, 'i7 6700HQ @ 2.60GHz\nprocessing 6,591,804 permutations per second', fontsize=7.5)
graph.figure.text(0.05, 0.02, 'Source: github.com/tappyy/qwertyuiop', fontsize=7.5)

# output graph to file
graph.figure.savefig('seaborn-graphs/alphanumerics-symbols.png')
