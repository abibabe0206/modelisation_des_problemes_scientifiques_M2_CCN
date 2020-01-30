def test(n):
    fb = []
    if n==0:
	return fb.append(1)
    elif n==1:
	return fb.append(1)
    else:
        fb = [1,1]
        for i in range(2,n):
            fb.append(fb[i-1] + fb[i-2])
        return fb

# the test section
# running the python section
# fb is the name of the file
import fb
fibo = fb.test(5)
print(fibo)

