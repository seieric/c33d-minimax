library(tidyverse)
(result <- read_csv(file="results.csv")) 
par(family = "Osaka")
theme_set(theme_gray(base_family = "Osaka"))
head(result)

summary(result)

# result$nodesの分布をグラフにする
(original_fig <- ggplot(data = result) + 
    geom_histogram(mapping = aes(nodes),
                   fill="skyblue",
                   colour="black",
                   alpha=0.5) +
    labs(x = "探索ノード数", y = "頻度")) +
  ggtitle("探索ノード数の分布")

# result$timeの分布をグラフにする
(original_fig <- ggplot(data = result) + 
    geom_histogram(mapping = aes(time),
                   fill="orange",
                   colour="black",
                   alpha=0.5) +
    labs(x = "計算時間", y = "頻度")) +
  ggtitle("計算時間の分布")

#nodesとtime散布図、回帰直線を引く
(original_fig <- ggplot(data = result) + 
    geom_point(mapping = aes(x = nodes, y = time),
               colour = "skyblue") +
    geom_smooth(mapping = aes(x = nodes, y = time),
                method = "lm",
                se = FALSE,
                colour = "orange") +
    labs(x = "探索ノード数", y = "計算時間")) +
  ggtitle("探索ノード数と計算時間の関係")

hist(result$nodes, breaks=40, col="skyblue", xlab="nodes", ylab="Frequency", main="Histogram of nodes")

# 密度分布をグラフにする
plot(density(result$nodes), col="skyblue", xlab="nodes", ylab="Density", main="Density plot of nodes")

# nodesとtimesの散布図を描く
plot(result$nodes, result$time, col="skyblue", xlab="探索ノード数", ylab="計算時間", main="探索ノード数と計算時間")
# 相関係数
cor(result$nodes, result$time)

# timesの分布をグラフにする
hist(result$time, breaks=20, col="skyblue", xlab="times", ylab="Frequency", main="Histogram of times")