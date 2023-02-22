#!/usr/bin/env ruby
# frozen_string_literal: true
require 'set'

class Array
  def map2d(&block)
    block_given? ? map { |row| row.map { |value| block.call(value) } } : to_enum(:map2d)
  end

  def map2di(&block)
    return enum_for :map2di unless block_given?
    each_with_index.map do |row, i|
      row.each_with_index.map { |x, j| block.call(x, i, j) }
    end
  end
end

class Range
  def **(other)
    to_a.repeated_permutation(other)
  end
end

def solve_sudoku(table)
  cells = table.map2di do |value, i, j|
    next [value] unless value.zero?
    (1..9).to_a - table[i] - (0..8).map { |k| table[k][j] } -
      ((0..2)**2).map { |di, dj| table[i / 3 * 3 + di][j / 3 * 3 + dj] } # TODO: slices?
  end
  candidates, i, j = cells.map2di.each.min_by { |x, _, _| x.length != 1 ? x.length : 10 }
  return [] if candidates.empty?
  return [cells.map2d(&:first)].each if candidates.length == 1
  Enumerator.new do |enum|
    candidates = (1..9).to_a - table[i] - (0..8).map { |k| table[k][j] } -
                 ((0..2)**2).map { |di, dj| table[i / 3 * 3 + di][j / 3 * 3 + dj] }
    candidates.each do |value|
      table[i][j] = value
      solve_sudoku(table).each { |x| enum.yield x }
    end
    table[i][j] = 0
  end
end

def main
  sudoku = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
  ]
  trap('SIGINT') { exit 130 }
  puts 'Trying to solve world hardest sudoku:'
  sudoku.each { |row| puts "\t#{row}" }
  start_time = Time.now
  solve_sudoku(sudoku).each_with_index do |table, i|
    time_spended = ((Time.now - start_time) * 1000).round
    puts "\nSolution ##{i + 1} found in #{time_spended} milliseconds:"
    table.each { |row| puts "\t#{row}" }
  end
end

main if __FILE__ == $PROGRAM_NAME