%Create t array
t=200:.01:300;

%Initialize constants
t0=(1366/2/5.67e-8/(1+.15))^.25;
alphai=.3;
alphaf=.7;
kappa=.1;

%Compute y values
alpha1=(t/t0).^4;
alpha2=alphai+.5*(alphaf-alphai)*(1+tanh(kappa*(t-273.15)));

%Make plots
plot(t,alpha1,'LineWidth',2)
hold on
plot(t,alpha2,'LineWidth',2)
hold off
legend('(T_s/T_0)^4)','\alpha(T_s)')
ax=gca;
ax.FontSize=20;
xlabel('Temperature (K)')
ylabel('Co-albedo')

cool=(alpha1>=alpha2);
change=(cool(2:end)~=cool(1:end-1));

%Both compute the same thing, it is plotted if the ; is omitted
%t(change);
t(change)
