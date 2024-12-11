const std = @import("std");
const eql = std.meta.eql;

const Order = struct {
    a: u32,
    b: u32,
    const Self = @This();
    pub fn format(
        self: Order,
        comptime fmt: []const u8,
        options: std.fmt.FormatOptions,
        writer: anytype,
    ) !void {
        _ = fmt;
        _ = options;

        try writer.print("{d}<{d}", .{ self.a, self.b });
    }
    pub fn init(a: u32, b: u32) Self {
        return Self{ .a = a, .b = b };
    }
};

fn parseInput(data: []u8) !struct { []Order, [][]u32 } {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    var order_list = std.ArrayList(Order).init(allocator);
    var update_list = std.ArrayList([]u32).init(allocator);

    var content = std.mem.split(u8, data, "\n\n");

    var orders_it = std.mem.split(u8, content.next().?, "\n");

    while (orders_it.next()) |order| {
        if (order.len == 0) {
            continue;
        }
        var it = std.mem.split(u8, order, "|");
        const l = try std.fmt.parseInt(u32, it.next().?, 10);
        const r = try std.fmt.parseInt(u32, it.next().?, 10);
        try order_list.append(Order.init(l, r));
    }

    var update_it = std.mem.split(u8, content.next().?, "\n");

    while (update_it.next()) |update| {
        if (update.len == 0) {
            continue;
        }

        var it = std.mem.split(u8, update, ",");
        var inner_updates = std.ArrayList(u32).init(allocator);
        while (it.next()) |u| {
            const uint = try std.fmt.parseInt(u32, u, 10);
            try inner_updates.append(uint);
        }

        try update_list.append(inner_updates.items);
    }

    return .{ order_list.items, update_list.items };
}

fn get_middle_value(data: []u32) u32 {
    return data[data.len / 2];
}

fn order_exists(orders: []Order, target: Order) bool {
    for (orders) |order| {
        if (eql(order, target)) {
            return true;
        }
    }
    return false;
}

fn part1(data: []u8) !i64 {
    const orders, const updates = try parseInput(data);

    var res: i64 = 0;

    for (updates) |update| {
        var valid = true;
        outer: for (update, 0..) |u_1, i| {
            for (update[i..]) |u_2| {
                const opp = Order.init(u_2, u_1);

                if (order_exists(orders, opp)) {
                    valid = false;
                    break :outer;
                }
            }
        }
        if (valid) {
            res += get_middle_value(update);
        }
    }
    return res;
}

fn part2(data: []u8) !i64 {
    const orders, const updates = try parseInput(data);

    var res: i64 = 0;
    for (updates) |update| {
        var valid = true;
        var fault = true;

        while (fault) {
            fault = false;
            for (update, 0..) |u_1, i| {
                for (update[i + 1 ..], i + 1..) |u_2, j| {
                    const opp = Order.init(u_2, u_1);
                    if (order_exists(orders, opp)) {
                        valid = false;
                        fault = true;
                        std.mem.swap(u32, &update[i], &update[j]);
                        break;
                    }
                }
            }
        }

        if (!valid) {
            res += get_middle_value(update);
        }
    }
    return res;
}

pub fn main() !void {
    const data = @embedFile("input/2024/05.txt");

    var t1 = std.time.nanoTimestamp();
    const p1 = try part1(@constCast(data));
    std.debug.print("p1: {d} in {d}s\n", .{ p1, @as(f128, @floatFromInt(std.time.nanoTimestamp() - t1)) / 10e9 });

    t1 = std.time.nanoTimestamp();
    const p2 = try part2(@constCast(data));
    std.debug.print("p2: {d} in {d}s\n", .{ p2, @as(f128, @floatFromInt(std.time.nanoTimestamp() - t1)) / 10e9 });
}
