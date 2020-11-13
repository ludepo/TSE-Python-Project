
# this script is just to store code for some types of plots, we can delete it later again

# Plot mean with confidence intervals
transactions['TIME'] = transactions['TIME'].astype(str)

# TODO: plot is ugly but if we need a plot with confidence intervals thats the code
trans_mean_day = transactions.groupby(by='TIME').mean().reset_index()
trans_std_day = transactions.groupby(by='TIME').std().reset_index()

plt.figure()
plt.plot(trans_mean_day.TIME, trans_mean_day.TURNOVER, trans_mean_day.TIPS)
plt.fill_between(trans_std_day.TIME, trans_mean_day.TURNOVER - 2 * trans_std_day.TURNOVER, trans_mean_day.TURNOVER + 2 * trans_std_day.TURNOVER, color="b", alpha=0.2)
plt.fill_between(trans_std_day.TIME, trans_mean_day.TIPS - 2 * trans_std_day.TIPS, trans_mean_day.TIPS + 2 * trans_std_day.TIPS, color="r", alpha=0.2)

