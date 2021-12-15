function [pos, ind] = get_all_pos(x,y)
    pos_num = nchoosek(sum(x==1),y);
    pos = zeros(pos_num,length(x));
    ind_temp = x==1;
    ind = repmat(ind_temp,pos_num,1);
    seed_perms = zeros(1,sum(x==1));
    seed_perms(1:y)=1;
    pos(:,ind_temp) = unique(perms(seed_perms),'rows');
end