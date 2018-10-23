#
#
#
#
#
# intab = "aeiou"
# outtab = "12345"
# # trantab = str.maketrans(intab, outtab,"xm")
# trantab = str.maketrans({"this":"asd"})
#
# str = "this is string example....wow!!!";
# print (str.translate(trantab))

a = [[1,2,3],[4,5,6],[7,8,9]]
idx_list = [ 0,2,1]
current_var_instantitation = [ a[x][idx_list[x]] for x in range(len(idx_list))]
print(current_var_instantitation)
