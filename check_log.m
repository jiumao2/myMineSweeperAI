fid = fopen('log.txt','r');
s = char(fread(fid));
a = str2num(s);
right_index = find(a==1);
per = length(right_index)/length(a);
figure;histogram(diff(right_index));title('ISI')
disp(['胜率为',num2str(per*100),'%'])

figure;
plot(1:length(a),cumsum(a)./(1:length(a))','x-');
title('Winning Rate vs Time')
xlabel('Number of trial')
ylabel('Winning Rate')
yline(0.35,'r--')