
clc
close all



%% Declaring gloabl variables and question#
global N_tot
N_tot = 1000; %Number of protons
prompt = 'What question you want to solve? ';
x = input(prompt);
question = x;

%% Declaring the variables 
if(question==1)
    tau_c = .1:.1:20; %Cloud optical thickness
    omega = [1,.9,.8]; %single scattering albedo
    theta_0 = 0; % Solar zenith angle
end

if(question==2)
    tau_c = 10;%Cloud optical thickness
    omega = [1,.96,.92,.88];%single scattering albedo
    theta_0 = 0; % Solar zenith angle
end

if(question==3)
    tau_c = .1:.1:50;%Cloud optical thickness
    omega = .8;%single scattering albedo
    theta_0 = pi/4;% Solar zenith angle
end

%% Computation of Reflectance,Absorption and Transmissiom

R = zeros(length(omega),length(tau_c)); %Reflectance
A = R; %Absorption
T = R; %Transmission
tau_star = zeros(N_tot,length(omega),length(tau_c)); %Deepest depth 

for i = 1:length(omega)
    for j = 1:length(tau_c)
        [N_ref,N_abs,N_tra,tau_star(:,i,j)] = computation(tau_c(j),omega(i),theta_0);
        R(i,j) = N_ref/N_tot; 
        A(i,j) = N_abs/N_tot;
        T(i,j) = N_tra/N_tot;
    end
end


%% Visualization for problem 1 and 2

if(question==1)
    hold on
    for i = 1:length(omega)
        plot(tau_c,R(i,:),'LineWidth',2)
    end
    hold off
    legend('\omega=1.0','\omega=0.9','\omega=0.8','Location','northwest')
    xlabel('\tau_c')
    ylabel('Reflectance')
    ax = gca;
    ax.FontSize = 20;
end

if(question==2)
    hold on
    for j = 1:length(omega)
        histogram(tau_star(:,j),0:.5:10,'Normalization','probability')
    end
    hold off
    legend('\omega=1.00','\omega=0.96','\omega=0.92','\omega=0.88','Location','northeast')
    ax = gca;
    ax.FontSize = 20;
end

%% Calculation function for problem 3

if(question==3)
    P = gammadist(tau_c);
    mean_R = .1*(.5*(P(1)*R(1)+P(end)*R(end))+sum(P(2:end-1).*R(2:end-1))); %Mean cloud reflectance
end

%% Applying monte carlo methods

function [N_ref,N_abs,N_tra,tau_star] = computation(tau_c,omega,theta_0)
global N_tot
tau_star = zeros(N_tot,1);
N_ref = 0;
N_abs = 0;
N_tra = 0;

y = tau_star;
ctheta = ones(N_tot,1)*cos(theta_0);
dest = y;
id = (1:N_tot)';
ld = N_tot;
while(ld)
    rng('shuffle')
    tau = -log(rand(ld,1));
    y(id) = y(id)+tau.*ctheta;
    dest(id(y(id)<=0)) = 1;
    dest(id(y(id)>=tau_c)) = 3;
    id = id(dest(id)==0);
    ld = length(id);
    isabsorbed = (rand(ld,1)>omega);
    dest(id(isabsorbed)) = 2;
    id = id(isabsorbed==0);
    ld = length(id);
    ctheta = 1-2*rand(ld,1);
    tau_star(id) = max(tau_star(id),y(id));
end

tau_star(dest>1) = NaN;
N_ref = sum(dest==1);
N_abs = sum(dest==2);
N_tra = sum(dest==3);
end

%% Function for probelm 3
function P = gammadist(tau)
C = .04;
k = .2;
P = C*tau.*exp(-k*tau);
end