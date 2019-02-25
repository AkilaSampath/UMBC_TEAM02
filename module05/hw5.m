% inputs
global N_tot
N_tot=10000;
tau_c=.1:.1:50;
omega=.8;
theta_0=pi/4;

% variables
dest=zeros(N_tot,length(tau_c),length(omega));
tau_star=dest;
R=zeros(length(tau_c),length(omega));
A=R;
T=R;

for i=1:length(tau_c)
    for j=1:length(omega)
        [N_ref,N_abs,N_tra,dest(:,i,j),tau_star(:,i,j)]=computation(tau_c(i),omega(j),theta_0);
        R(i,j)=N_ref/N_tot;
        A(i,j)=N_abs/N_tot;
        T(i,j)=N_tra/N_tot;
    end
end

% hold on
% plot(tau_c,R(:,1),'LineWidth',2)
% plot(tau_c,R(:,2),'LineWidth',2)
% plot(tau_c,R(:,3),'LineWidth',2)
% hold off
% legend('\omega=1.0','\omega=0.9','\omega=0.8','Location','northwest')
% ax=gca;
% ax.FontSize=20;

% hold on
% histogram(tau_star(dest(:,1,1)==1,1,1))
% histogram(tau_star(dest(:,1,2)==1,1,2))
% histogram(tau_star(dest(:,1,3)==1,1,3))
% histogram(tau_star(dest(:,1,4)==1,1,4))
% hold off
% legend('\omega=1.00','\omega=0.96','\omega=0.92','\omega=0.88','Location','northwest')
% ax=gca;
% ax.FontSize=20;

P=gammadist(tau_c');
mean_R=.1*(.5*(P(1)*R(1)+P(end)*R(end))+sum(P(2:end-1).*R(2:end-1)));

function [N_ref,N_abs,N_tra,dest,tau_star]=computation(tau_c,omega,theta_0)

[dest,tau_star]=photon(tau_c,omega,theta_0);

% output
N_ref=sum(dest==1);
N_abs=sum(dest==2);
N_tra=sum(dest==3);
end

function [dest,tau_star]=photon(tau_c,omega,theta_0)
global N_tot
y=zeros(N_tot,1);
dest=y;
tau_star=y;
isabsorbed=y;
theta=repmat(theta_0,[N_tot,1]);
id=ones(N_tot,1);
ld=N_tot;

while(ld)
    f=rand(ld,1);
    tau=-log(f);
    y(id)=y(id)+tau.*cos(theta);
    tau_star(id)=max([tau_star(id);y(id)]);
    dest(id & y<0)=1;
    dest(id & y>=tau_c)=3;
    id=(dest==0);
    ld=sum(id);
    isabsorbed(id)=(rand(ld,1)>omega);
    dest(id & isabsorbed)=2;
    id=(dest==0);
    ld=sum(id);
    theta=rand(ld,1)*pi;
end
tau_star(tau_star>tau_c)=tau_c;
end

function P=gammadist(tau)
C=.04;
k=.2;
P=C*tau.*exp(-k*tau);
end