const std = @import("std");

fn parseInput(data: []u8) ![][]u32 {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    var levels = std.ArrayList([]u32).init(allocator);

    var line_it = std.mem.split(u8, data, "\n");

    while (line_it.next()) |line| {
        if (line.len == 0) {
            continue;
        }
        var inner = std.ArrayList(u32).init(allocator);
        var it = std.mem.split(u8, line, " ");
        while (it.next()) |num| {
            const n = try std.fmt.parseInt(u32, num, 10);
            try inner.append(n);
        }
        try levels.append(inner.items);
    }

    return levels.items;
}

fn sign_change(old: i64, new: i64) bool {
    return (old < 0 and new > 0) or (old > 0 and new < 0);
}

fn is_valid(level: []u32, index: usize) bool {
    var shift: u32 = 0;
    if (index == 0) {
        shift = 1;
    }
    var val: u32 = level[0 + shift];
    var diff: i64 = 0;

    for (level[(1 + shift)..], (1 + shift)..) |l, i| {
        if (i == index) {
            continue;
        }
        const d = @as(i64, val) - @as(i64, l);
        if (d == 0 or @abs(d) > 3 or sign_change(diff, d)) {
            return false;
        }

        val = l;
        diff = d;
    }

    return true;
}

fn part1(data: []u8) !u64 {
    const levels = try parseInput(data);

    var res: u64 = 0;
    for (levels) |level| {
        if (is_valid(level, level.len)) {
            res = res + 1;
        }
    }
    return res;
}

fn part2(data: []u8) !u64 {
    const levels = try parseInput(data);

    var res: u64 = 0;
    for (levels) |level| {
        for (0..level.len) |i| {
            if (is_valid(level, i)) {
                res = res + 1;
                break;
            }
        }
    }

    return res;
}

pub fn main() !void {
    const data = @embedFile("input/2024/02.txt");

    const p1 = try part1(@constCast(data));
    const p2 = try part2(@constCast(data));

    std.debug.print("p1: {d}\n", .{p1});
    std.debug.print("p2: {d}\n", .{p2});
}
