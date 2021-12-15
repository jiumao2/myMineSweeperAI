opt = optimoptions('fmincon','StepTolerance',1e-5);
while true
    fid = fopen('info.txt','r');
    a = fread(fid);
    fclose(fid);
    if a == '1'
        x0 = csvread('x.csv');
        y0 = csvread('y.csv');
        output = fmincon(@(t)norm(t),rand(size(x0,2),1),[-1*eye(size(x0,2));eye(size(x0,2))],...
            [zeros(size(x0,2),1);ones(size(x0,2),1)],x0,y0,[],[],[],opt);
        csvwrite('output.csv',output);
        fid = fopen('info.txt','w');
        fwrite(fid,'0');
        fclose(fid);
    end
end