const std = @import("std");
const eql = std.mem.eql;
const max = std.sort.max;

fn parseInput(data: []u8) ![][]u8 {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    var vals = std.ArrayList([]u8).init(allocator);

    var line_it = std.mem.split(u8, data, "\n");

    while (line_it.next()) |line| {
        if (line.len == 0) {
            continue;
        }
        try vals.append(@constCast(line));
    }

    return vals.items;
}

fn in_bounds(vals: [][]u8, x: isize, y: isize) bool {
    return x < vals[0].len and x >= 0 and y < vals.len and y >= 0;
}

fn is_word(word: []const u8, vals: [][]u8, x: isize, y: isize, dx: isize, dy: isize) bool {
    const l: isize = @intCast(word.len);
    if (!in_bounds(vals, x + (dx * (l - 1)), y + (dy * (l - 1)))) {
        return false;
    }

    for (0..word.len) |i_0| {
        const i: isize = @as(isize, @intCast(i_0));
        const ny: usize = @as(usize, @intCast(y + (dy * i)));
        const nx: usize = @as(usize, @intCast(x + (dx * i)));
        if (vals[ny][nx] != word[i_0]) {
            return false;
        }
    }

    return true;
}

fn count(vals: [][]u8, x: isize, y: isize) u32 {
    var r: u32 = 0;

    for (0..3) |dy0| {
        for (0..3) |dx0| {
            const dy: isize = @as(isize, @intCast(dy0)) - 1;
            const dx: isize = @as(isize, @intCast(dx0)) - 1;
            if ((dy == 0 and dx == 0) or !in_bounds(vals, x + dx, y + dy)) {
                continue;
            }

            if (is_word("XMAS", vals, x, y, dx, dy)) {
                r += 1;
            }
        }
    }
    return r;
}

fn is_cross(word: [3]u8, vals: [][]u8, x: usize, y: usize) bool {
    if (vals[y][x] != word[1]) {
        return false;
    }

    if (!(x > 0 and y > 0 and x + 1 < vals[0].len and y + 1 < vals.len)) {
        return false;
    }

    const tl = vals[y - 1][x - 1];
    const br = vals[y + 1][x + 1];

    const tr = vals[y - 1][x + 1];
    const bl = vals[y + 1][x - 1];

    return ((tl == word[0] and br == word[2]) or (tl == word[2] and br == word[0])) and
        ((tr == word[0] and bl == word[2]) or (tr == word[2] and bl == word[0]));
}

fn part1(data: []u8) !i64 {
    const vals = try parseInput(data);

    var res: i64 = 0;

    const h = vals.len;
    const w = vals[0].len;

    for (0..h) |y| {
        for (0..w) |x| {
            res += count(vals, @intCast(x), @intCast(y));
        }
    }

    return res;
}

fn part2(data: []u8) !i64 {
    const vals = try parseInput(data);

    var res: i64 = 0;

    const h = vals.len;
    const w = vals[0].len;

    for (0..h) |y| {
        for (0..w) |x| {
            if (is_cross("MAS".*, vals, x, y)) {
                res += 1;
            }
        }
    }
    return res;
}

pub fn main() !void {
    const data = @embedFile("input/2024/04.txt");

    var t1 = std.time.nanoTimestamp();
    const p1 = try part1(@constCast(data));
    std.debug.print("p1: {d} in {d}s\n", .{ p1, @as(f128, @floatFromInt(std.time.nanoTimestamp() - t1)) / 10e9 });

    t1 = std.time.nanoTimestamp();
    const p2 = try part2(@constCast(data));
    std.debug.print("p2: {d} in {d}s\n", .{ p2, @as(f128, @floatFromInt(std.time.nanoTimestamp() - t1)) / 10e9 });
}
