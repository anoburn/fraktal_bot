#include <SFML/System.hpp>
#include <SFML/Window.hpp>
#include <SFML/Graphics.hpp>
#include <iostream>
#include <ctime>
#include <cmath>

int calc_iterations(double x_pos, double y_pos, int max_iteration, float c_re, float c_im) {
	double x = x_pos;
	double y = y_pos;
	double xtemp;
	int iteration = 0;

	while ((x*x + y*y < 4) & (iteration < max_iteration)) {
		xtemp = x*x - y*y + c_re;
		y = 2 * x*y + c_im;
		x = xtemp;
		iteration++;
	}

	return iteration;
}


sf::Color find_color(int iterations, int max_iterations) {

	int dif_r, dif_g, dif_b, red, green, blue;
	sf::Color left, right;

	sf::Color color_set = sf::Color::Black;
	if (iterations >= max_iterations)
		return color_set;

	//const int n_colors = 4;
	sf::Color color0(100, 0, 100, 255);
	sf::Color color1(0, 0, 255, 255);
	sf::Color color2(0, 255, 0, 255);
	sf::Color color3(255, 0, 0, 255);

	sf::Color colors[] = { color0, color1, color2, color3};
	
	int n_colors = sizeof(colors) / sizeof(colors[0]);

	//std::cout << "length of array: " << length << "\n";
	
	
	float fraction = fmod(iterations, max_iterations / (n_colors-1.)) / (max_iterations / (n_colors-1.));
	//std::cout << "iterations: " << iterations << ", fraction: " << fraction << "\n";

	int color_index = iterations / (max_iterations / (n_colors - 1.));
	left  = colors[color_index];
	right = colors[color_index + 1];

	dif_r = right.r - left.r;
	dif_g = right.g - left.g;
	dif_b = right.b - left.b;

	red   = left.r + (dif_r * fraction);
	green = left.g + (dif_g * fraction);
	blue  = left.b + (dif_b * fraction);

	sf::Color color(red, green, blue, 255);

	return color;
}


void show_color_gradient(sf::RenderWindow& window) {
	sf::Vector2u size = window.getSize();
	sf::Image image;
	image.create(size.x, size.y);


	for (int x = 0; x < size.x; x++) {
		sf::Color color = find_color(x, size.x);
		for (int y = 0; y < size.y; y++) {
			image.setPixel(x, y, color);
		}
	}

	sf::Texture texture;
	texture.loadFromImage(image);
	sf::Sprite sprite;
	sprite.setTexture(texture);

	window.clear();
	window.draw(sprite);
	window.display();
	
	return;
}


// Function when c_re and c_im are given
void update_img(sf::Image& image, float x_low, float x_high, float y_low, float y_high,
				int max_iteration, float c_re, float c_im) {
	sf::Vector2u size = image.getSize();

	float x_step = (x_high - x_low) / size.x;
	float y_step = (y_high - y_low) / size.y;
	float x0, y0;

	for (unsigned int x = 0; x < size.x; x++) {
		for (unsigned int y = 0; y < size.y; y++) {
			x0 = x_low + x * x_step;
			y0 = y_low + y * y_step;
			int iterations = calc_iterations(x0, y0, max_iteration, c_re, c_im);
			//std::cout << iterations << " iterations at " << x0 << ", " << y0 << "\n";
			
			image.setPixel(x, y, find_color(iterations, max_iteration));
		}
	}
}


// No constant given. Calculates the Mandelbrot set
void update_img(sf::Image& image, float x_low, float x_high, float y_low, float y_high,
	int max_iteration) {
	sf::Vector2u size = image.getSize();

	float x_step = (x_high - x_low) / size.x;
	float y_step = (y_high - y_low) / size.y;
	float x0, y0;

	for (unsigned int x = 0; x < size.x; x++) {
		for (unsigned int y = 0; y < size.y; y++) {
			x0 = x_low + x * x_step;
			y0 = y_low + y * y_step;
			int iterations = calc_iterations(x0, y0, max_iteration, x0, y0);
			//std::cout << iterations << " iterations at " << x0 << ", " << y0 << "\n";

			image.setPixel(x, y, find_color(iterations, max_iteration));
		}
	}
}



int main(int argc, char** argv) {
	int x_border = atoi(argv[5]);
	int y_border = atoi(argv[6]);
	float stretch = x_border * 1. / y_border;
	int N = x_border * y_border;
	//bool paused = false;
	bool mandelbrot = true;
	float c_re, c_im;

	double x_center = atof(argv[1]);
	double y_center = atof(argv[2]);

	float zoom = atof(argv[3]);
	float booster = 1.;

	double x_low  = x_center - zoom * stretch;
	double x_high = x_center + zoom * stretch;
	double y_low  = y_center - zoom;
	double y_high = y_center + zoom;



	int max_iteration = atoi(argv[4]);

	std::cout << argv[0] << "\n";

	sf::Image image;
	image.create(x_border, y_border);
	update_img(image, x_low, x_high, y_low, y_high, max_iteration);
	image.saveToFile("fraktal.png");

	return 0;
}
