# Plot Heatmap with Transparent Background
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_alpha(0)  # Make figure background transparent
ax.set_facecolor('none')  # Make axis background transparent

# Plot heatmap
sns.heatmap(df, cmap="coolwarm", annot=False, ax=ax)

# Make text white
ax.xaxis.label.set_color("white")  # X-axis label color
ax.yaxis.label.set_color("white")  # Y-axis label color
ax.tick_params(colors="white")  # Tick labels color
ax.spines[:].set_color("white")  # Make spines white

st.pyplot(fig)
