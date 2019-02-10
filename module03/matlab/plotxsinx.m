x = [-2*pi : 4*pi/1024 : 2*pi];
y = x .* sin(x.^2);
H = plot (x,y);
set(H,'LineWidth',2)
axis on
grid on
title ('Graph of f(x)=x sin(x^2)')
xlabel ('x')
ylabel ('f(x)')
xlim ([-2*pi 2*pi])

