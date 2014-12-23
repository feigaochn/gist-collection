// $ clang++ -std=c++1y -pedantic -Wall -stdlib=libc++ test_01.cpp -o test_01
// $ g++-4.9.1 -std=c++14 -pedantic -Wall test_01.cpp -o test_01

#include<iostream>
#include<complex>
#include<algorithm>
#include<vector>

void square() {
	// Store a generalized lambda, that squares a number, in a variable
	auto func = [](auto input) { return input * input; };

	// Usage examples:
	// square of an int
	std::cout << func(10) << std::endl;

	// square of a double
	std::cout << func(2.345) << std::endl;

	// square of a complex number
	std::cout << func(std::complex<double>(3, -2)) << std::endl;
}

void sorting() {
	std::vector<int> V(10);

	// Use std::iota to create a sequence of integers 0, 1, ...
	std::iota(V.begin(), V.end(), 1);

	// Print the unsorted data using std::for_each and a lambda
	std::cout << "Original data" << std::endl;
	std::for_each(V.begin(), V.end(), [](auto i) { std::cout << i << " "; });
	std::cout << std::endl;

	// Sort the data using std::sort and a lambda
	std::sort(V.begin(), V.end(), [](auto i, auto j) { return (i > j); });

	// Print the unsorted data using std::for_each and a lambda
	std::cout << "Sorted data" << std::endl;
	std::for_each(V.begin(), V.end(), [](auto i) { std::cout << i << " "; });
	std::cout << std::endl;
}


int main() {
	square();
	sorting();
	return 0;
}