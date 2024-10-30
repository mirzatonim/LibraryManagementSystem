# # Enter your code here. Read input from STDIN. Print output to STDOUT
# thickness = 5

# c = 'H'

# for i in range(thickness):
#     print((c * (2*i + 1)).center(thickness * 2))
    
# for i in range(thickness + 1):
#     print((c * thickness).center(thickness * 2) + (c * thickness).center(thickness * 6))
    
# for i in range((thickness + 1) // 2):
#     print((c * thickness * 5).center(thickness * 6))

# for i in range(thickness + 1):
#     print((c * thickness).center(thickness * 2) + (c * thickness).center(thickness * 6))
    
# for i in range(thickness):
#     print((c * (thickness - i)).rjust(thickness * 3).rjust(thickness * 6))
    
# # for i in range(thickness):
# #     print((c * (2*(thickness - i) - 1)).rjust(thickness * 3).rjust(thickness * 6))

# # for i in range(thickness):
# #     print(((c*(thickness-i-1)).rjust(thickness)+c+(c*(thickness-i-1)).ljust(thickness)).rjust(thickness*6))
# def print_mirza_logo():
#     # Each line corresponds to a line in the logo for the word "MIRZA"
#     lines = [
#         "MM     MM   IIIII    RRRR    ZZZZZ   AAAAA",
#         "MMM   MMM     I      R   R      Z    A   A",
#         "MMM MM MMM     I      RRRR      Z     AAAAA",
#         "MM  MM  MM     I      R  R     Z      A   A",
#         "MM     MM   IIIII    R   R   ZZZZZ   A   A"
#     ]
    
#     for line in lines:
#         print(line)

# # Call the function to print the logo
# print_mirza_logo()

# def solve(s):
#     s = s.split()

#     for i in range(len(s)):
#         if s[i][0].isalpha():
#             s[i] = s[i][0].capitalize() + s[i][1:]
#     return ' '.join(s)
   

        
  

# if __name__ == "__main__":

#     s = "hello world 12abc a43"
#     result = solve(s)
#     print(result)

############################################3

# def reverse_str(s):
  
#     ns = s.split()
#     for x in ns:
#         x = x[::-1]
#         print(x, end=' ')

# if __name__ == '__main__':
#     s = "Hello Mirza Tonim"
#     rev_str = reverse_str(s)
#     # print(rev_str)

#################################################

# def ispalidrome(s):
#     if s == s[::-1]:
#         return True
#     else:
#         return False

# if __name__ == '__main__':

#     s = "madam"
#     result = ispalidrome(s)
#     print(result)

#################################################

# def count_vowel_conso(s):
#     vowels = ['a', 'e', 'i', 'o', 'u']
    
#     result = ""

#     for char in s:
#         if char in vowels:
#             result += '*'
#         else:
#             result += char
#     return result
            
        
    #    print(i)



    # count1 = 0
    # count2 = 0
    # for i in ss:
    #     if i in vowels:
    #         count1 += 1
    #     else:
    #         count2 += 1
    # return (f"Vowels: {count1}, Consonants: {count2}")



# if __name__ == "__main__":

#     s = "example"
#     res = count_vowel_conso(s)
#     print(res)

##################################################

# def find_str(s, subs):
#     if subs in s.casefold():
#         print(True)

# if __name__ == '__main__':

#     s = 'Hello World'
#     subs = 'world'

#     res = find_str(s, subs)

##########################################

# def isLeapYear(year):
    
#     if (year % 400 == 0) or ((year % 100 != 0) and (year % 4 == 0)):
#         return True
#     else:
#         return False

# if __name__ == '__main__':

#     year = int(input())

#     result = isLeapYear(year)
#     print(result)
    
#############################################3

# def even_odd(num):
#     if num % 2 == 0:
#         print('even')
#     else:
#         print('odd')

# if __name__ == '__main__':

#     num = int(input())
#     res = even_odd(num)
#     # print(res)
################################################
# def find_max_min(a):
#     ns = map(int, a)
#     add = 0

#     nz = list(ns)
#     for x in nz:
#         add += x
#         avg = add / len(nz)
#     # m_v = min(nz)
#     print('{:.2f}'.format(avg))

# if __name__ == '__main__':

#     nums = 4, 12, 7
#     res = find_max_min(nums)
##################################################

# def sum_digit(num):
#     numbers = map(int, num)
#     numss = list(numbers)
#     a = 0
#     for x in numss:
#         a += x
#     print(a)

# if __name__ == '__main__':

#     n = input()
#     res = sum_digit(n)
##################################################



