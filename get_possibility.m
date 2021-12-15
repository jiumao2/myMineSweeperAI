while true
    fid = fopen('info.txt','r');
    a = fread(fid);
    fclose(fid);
    if a == '2'
        x0 = csvread('x.csv');
        y0 = csvread('y.csv');
        total_bomb = 99;
        
        to_include = [];
        x2 = [];
        x2_all = [];
        for k = 1:size(x0,1)
            x2 = [x2;x0(k,:)];
            if rank(x2)>rank(x2_all)
                x2_all = x2;
                to_include = [to_include,k];
            end
        end
        x0 = x0(to_include,:);
        y0 = y0(to_include);
        for k = 2:size(x0,1)
            for j = 2:size(x0,1)
                if k~=j
                    ind1 = find(x0(k,:)==1);
                    ind2 = find(x0(j,:)==1);
                    if length(union(ind1,ind2)) == length(ind1) && all(union(ind1,ind2)==ind1)
                        x0(k,ind2)=0;
                        y0(k)=y0(k)-y0(j);
                    elseif length(union(ind1,ind2)) == length(ind2) && all(union(ind1,ind2)==ind2)
                        x0(j,ind1)=0;
                        y0(j)=y0(j)-y0(k);
                    end
                end
            end
        end
        
        if size(x0,1)>1
        % we need a 
        % list all possibilities of x0(2:end)
            [pos,ind] = get_all_pos(x0(2,:),y0(2));
            for k =3:size(x0,1)
                [pos_new,ind_new] = get_all_pos(x0(k,:),y0(k));
                if k>2
                    [pos,ind] = compare_two_pos(pos,ind,pos_new,ind_new);
                    pos_ind = unique([pos,ind],'rows');
                    pos = pos_ind(:,1:size(x0,2));
                    ind = pos_ind(:,size(x0,2)+1:end);
                    
                    if size(pos,1)>100
                        temp = randperm(size(pos,1),size(pos,1)-100);
                        pos(temp,:)=[];
                        ind(temp,:)=[];
                    end
                end
            end
            % last deal with first equation
            weights = zeros(size(pos,1),1);
            for k = 1:size(pos,1)
               temp_ind = 1:size(x0,2);
               temp_ind(ind(k,:)==1)=[];
               to_delete = [];
               if total_bomb-sum(pos(k,:))>0 && length(temp_ind) >= total_bomb-sum(pos(k,:))
                   pos(k,temp_ind) = round(total_bomb-sum(pos(k,:)))/length(temp_ind);
                   weights(k) = nchoosek(length(temp_ind),round(total_bomb-sum(pos(k,:))));
               elseif total_bomb-sum(pos(k,:))==0
                   pos(k,temp_ind) = 0;
                   weights(k) = 1;
               else
                   to_delete = [to_delete,k];
               end
            end
            pos(to_delete,:)=[];
            weights(to_delete) = [];
            weights = weights./sum(weights);
            % compute possibility of each block
            pos_all = pos'*weights;
        else
            pos_all = total_bomb/size(x0,2)*ones(size(x0,2),1);
        end
        csvwrite('output.csv',pos_all);
        fid = fopen('info.txt','w');
        fwrite(fid,'0');
        fclose(fid);
    end
end