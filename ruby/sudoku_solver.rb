#!/usr/bin/env ruby
# frozen_string_literal: true

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

class Sudoku
  def initialize(cells = (1..9).map { (1..9).map { (1..9).to_a } })
    @cells = cells
  end

  def clone
    Sudoku.new @cells.map(&:clone)
  end

  def to_s
    @cells.map { |r| r.map { |x| x.length == 1 ? x.first : '-' }.join ' ' }.join "\n"
  end

  def []=(row, column, value)
    # puts "[]= #{row} #{column} #{value}"
    raise 'Conflict' unless @cells[row][column].include? value
    return unless @cells[row][column].length > 1

    @cells[row][column] = [value]
    queue = [[row, column]]
    until queue.empty?
      queue.delete(index = queue.first)
      i0, j0 = index
      value = @cells[i0][j0].first
      neighbors = ((0..8).to_a.product([j0]) + [i0].product((0..8).to_a) +
        ((0..2)**2).map { |i, j| [i0 / 3 * 3 + i, j0 / 3 * 3 + j] }) - [[i0, j0]]
      neighbors.each do |i, j|
        next unless @cells[i][j].include? value
        queue.append [i, j] if (@cells[i][j] -= [value]).length == 1
        raise 'Conflict' if @cells[i][j].empty?
      end
    end
  end

  def solutions
    candidates, i, j = @cells.map2di.min_by { |x, _, _| (x.length - 2) % 10 }
    return [self].to_enum if candidates.length == 1

    Enumerator.new do |enum|
      candidates.each do |candidate|
        sudoku = clone
        begin
          sudoku[i, j] = candidate
          sudoku.solutions.each { |solution| enum.yield solution }
        rescue
        end
      end
    end
  end
end

def main
  table = [
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
  sudoku = Sudoku.new
  table.map2di { |x, i, j| sudoku[i, j] = x if x != 0 }
  trap('SIGINT') { exit 130 }
  puts 'Trying to solve world hardest sudoku:'
  puts sudoku
  start_time = Time.now
  sudoku.solutions.each_with_index do |table, i|
    time_spended = ((Time.now - start_time) * 1000).round
    puts "\nSolution ##{i + 1} found in #{time_spended} milliseconds:"
    puts table
  end
  time_spended = ((Time.now - start_time) * 1000).round
  puts "\nFinished in #{time_spended} milliseconds."
end

main if __FILE__ == $PROGRAM_NAME
