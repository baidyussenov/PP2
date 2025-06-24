def is_palindrome(s):
    return s == s[::-1]

print(is_palindrome("radar"))  # palindrom
print(is_palindrome("hello"))  # not palindrom