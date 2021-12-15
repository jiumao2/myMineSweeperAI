function [pos_out, ind_out] = compare_two_pos(pos,ind,pos_new,ind_new)
    pos_out = [];
    ind_out = [];
    for k = 1:size(pos,1)
        for j = 1:size(pos_new,1)
            pos_k = pos(k,:);
            ind_k = ind(k,:)==1;
            pos_new_j = pos_new(j,:);
            ind_new_j = ind_new(j,:)==1;
            temp = intersect(find(ind_k),find(ind_new_j));
            if all(pos_k(temp)==pos_new_j(temp))
                temp_ind_out = zeros(1,length(pos_k));
                temp_ind_out(ind_k)=1;
                temp_ind_out(ind_new_j)=1;
                ind_out = [ind_out;temp_ind_out];
                
                pos_k(pos_new_j==1)=1;
                pos_out = [pos_out;pos_k];
            end
        end
    end
end