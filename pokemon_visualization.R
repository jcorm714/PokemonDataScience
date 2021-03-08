library(lattice)


pokemon <- read.csv("pokemon.csv")

attach(pokemon)
head(pokemon)

#  g <- ggplot(pokemon, aes(x=Tier, y=Stat.Total, "Pokemon Tier Based off Stat Total")) + geom_boxplot()
# g

notUsedTiers <- list("NFE", "National Dex", "LC", "AG","")

tiers = unique(pokemon$Tier)
tiers = sort(tiers, decreasing = TRUE)
tiers = tiers[tiers != "NFE"]
tiers = tiers[tiers != "National Dex"]
tiers = tiers[tiers != "LC"]
tiers = tiers[tiers != "AG"]
tiers = tiers[tiers != ""]

tiers 

tiers = factor(tiers, levels=c(4.0, 3.5, 5, 3, 2.5, 1, 4.5,2,1.5))
tiers = sort(tiers)

cloud(O.Score-D.Score*T)
