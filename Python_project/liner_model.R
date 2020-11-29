data <- read.csv("experiment_data.csv", header = F)

head(data)

range(data$V7)
data$V1 <- as.factor(data$V1)
data$V2 <- as.factor(data$V2)
data$V3 <- as.factor(data$V3)
data$V4 <- as.factor(data$V4)
data$V5 <- as.factor(data$V5)
data$V6 <- as.factor(data$V6)
data$V7


fit <- lm(V7 ~ V1*V3*V5, data = data)
summary(fit)
