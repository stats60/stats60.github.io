# Create a vector filled with random normal values
u1 <- rnorm(30)

# This loop calculates the square of the first 10 elements of vector u1

# Initialize `usq`
usq <- array(NA, 10)

for(i in 1:10) {
  # i-th element of `u1` squared into `i`-th position of `usq`
  usq[i] <- u1[i]*u1[i]
  print(usq[i])
}

# Create a 30 x 30 matrix (of 30 rows and 30 columns)
mymat <- matrix(NA, nrow=30, ncol=30)

# For each row and for each column, assign values based on position: product of two indexes
for(i in 1:dim(mymat)[1]) {
  for(j in 1:dim(mymat)[2]) {
    mymat[i,j] = i*j
  }
}

# Just show the upper left 10x10 chunk
mymat[1:10, 1:10]

#while (condition)
#{
#  statement
#}


# while loop in R

i <- 1
while (i <=6) {
  print(i*i)
  i = i+1
}

#if (test_expression) {
#  statement
#}

x <- 5
if(x > 0){
  print("Positive number")
}

#if (test_expression) {
#  statement1
#} else {
#  statement2
#}

x <- -5
if(x >= 0){
  print("Non-negative number")
} else {
  print("Negative number")
}

#if ( test_expression1) {
#  statement1
#} else if ( test_expression2) {
#  statement2
#} else if ( test_expression3) {
#  statement3
#} else {
#  statement4
#}

x <- 0
if (x < 0) {
  print("Negative number")
} else if (x > 0) {
  print("Positive number")
} else
  print("Zero")