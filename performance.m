%performance study
a = [1,2,4,8,16];%ppn
n = [10,10,7,3,1];
n1 = [96,48,43,37,18];
n2 = [861,393,359,289,152];
n3 = [861,393,359,289,152];
n4 = [861,393,359,289,152];
n5 = [861,393,359,289,152];
figure(1)
loglog(a,n,'k-',a,n1,'g',a,n2,'c-*',a,n3,'m-',a,n4,'y--',a,n5,'r-')
legend('N =1024,n=1','N =2048,n=1','N =4096,n=1','N =8192,n=1','N =16384,n=1')
xlabel('Number of parallel processes')
ylabel('Seconds')
title('Observed efficiency')
