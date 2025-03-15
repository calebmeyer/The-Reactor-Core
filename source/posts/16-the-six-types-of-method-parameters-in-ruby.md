---
date: 2025-03-11T16:02:15
pageTitle: 16 - The Six Types of Method Parameters in Ruby
tags: posts
---

Ruby is an amazingly expressive language, and it hasn't been afraid to evolve over the years. These are the six types of parameters, and when they were introduced.

## Aside: Parameters vs Arguments

Before we start, I'd like to clear up a common source of confusion.

When you define a method, you are specifying its parameters:

```ruby
def rename(from, to:) # from and to are parameters to this method
```

And when you call it, you are passing arguments to that method:

```ruby
hash.rename(:facility_id, to: :store_code)
```

## 1. Positional Parameters

These are by far the most common type of argument, and the only type I've seen available in every programming language I've used. Positional arguments are passed by their position in the parameter list:

```ruby
def calculate_interest(principal, rate, years)
  principal * rate * years
end

calculate_interest(100_000, 6.68.to_percent, 30)
```

Positional parameters are easy to understand, and great for methods with few parameters. As far as I can tell, both this and the next type have been in ruby since the beginning (certainly longer than I've been programming ruby).

## 2. Defaulted Positional Parameters

Sometimes you want to allow a parameter to be optional. You can specify a default value for it with `=`:

```ruby
def calculate_interest(principal, rate = 6.68.to_percent, years = 30)
  principal * rate * years
end

calculate_interest(150_000, 6.68.to_percent)
```

These default values can be based on earlier parameters, as well:

```ruby
def color(red=256, blue=red, green=blue / 2) # I know, the order will come up later
```

## 3. Keyword Parameters

Keyword parameters were introduced in ruby 2.0 and allow you to name your arguments.

Prior to their introduction, it was common to see methods like this:

```ruby
def get(url, options = {})
```

Without reading the method documentation, you had no way of knowing how to call this method. You could pass anything in that options hash, even if it didn't make sense:

```ruby
get('http://httpbin.org/get', status: 500, with: :ferocity)
```

Similarly, if I used the above color method with the expected order for the values (RGB), it would produce the wrong color:

```ruby
red, green, blue = [256, 128, 64]
color(red, green, blue) #=> rgb(256, 64, 128)
```

If you use keyword parameters, then any callers of a method are required to specify which argument they mean. It makes call sites much easier to read.

```ruby
def color(blue:, green:, red:)

# then much later in another file
color(red: 256, green: 128, blue: 64)
```

## 4. Defaulted Keyword Parameters

Keyword parameters would be less useful than positional parameters if they didn't also support default values. Fortunately, they do, with about the syntax you'd expect:

```ruby
calculate_interest(principal:, rate: 6.68.to_percent, years: 30)
```

Now when you call this method, it's very clear what each parameter does, and you can skip any defaults you don't feel like passing:

```ruby
calculate_interest(principal: 200_000, years: 15)
```

## 5. Splat Parameter

Sometimes, you don't know what arguments will be coming into a method. If you want to collect them into an array, you can use a `*` (splat):

```ruby
def sum(*numbers)
  numbers.reduce(:+)
end

sum(1, 2, 3) #=> 6
```

You can use a splat in any position, but you can only use one:

```ruby
def word(prefix, *middle_parts, suffix)
  puts prefix + middle_parts.join('') + suffix
end

word('pain', 'stak', 'ing', 'ly')
```

## 6. Double Splat Parameter

Just like you can use `*[1, 2, 3]` to spread out an array, you can use `**{ some: 'hash' }` to spread out a hash:

```ruby
address = { nice: 'try' }
person = { id: 1, name: 'Caleb', **address }
```

Parameters work the same way. You can specify any number of additional keyword parameters with a double splat.

```ruby
def initialize(**attributes)
  attributes.each { |key, value| cache[key] = value }
  super
end
```

## Bonus: Block Parameters

Blocks are similar to methods, but have different ways to do parameters.

### Positional

```ruby
Author.books.each { |book| puts book.title }

Hash.each { |key, value| puts "#{key}: #{value}" }
```

### Numbered

You can also refer to a block's parameters using numbered parameters, though I haven't seen it very often in practice.

```ruby
class ApiBackedModel
  def where
    http_response.to_json.each { new(_1) }
  end
end
```

This feature was introduced in Ruby 2.7.

### it Rocks

And in Ruby 3.4, a new parameter `it` was introduced. `it` is always the first parameter to a block, if you don't define any parameters.

```ruby
def title_case(string)
  string.split.map { it.capitalize }
end
```
