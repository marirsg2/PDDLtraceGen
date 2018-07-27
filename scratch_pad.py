




intab = "aeiou"
outtab = "12345"
# trantab = str.maketrans(intab, outtab,"xm")
trantab = str.maketrans({"this":"asd"})

str = "this is string example....wow!!!";
print (str.translate(trantab))