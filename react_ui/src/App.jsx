import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from 'recharts';
import { AlertCircle, TrendingUp, Activity, Calendar } from 'lucide-react';

const App = () => {
    const [data, setData] = useState([]);
    const [events, setEvents] = useState([]);
    const [impact, setImpact] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedEvent, setSelectedEvent] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [resPrices, resEvents, resImpact] = await Promise.all([
                    axios.get('/api/historical'),
                    axios.get('/api/events'),
                    axios.get('/api/impact')
                ]);
                setData(resPrices.data);
                setEvents(resEvents.data);
                setImpact(resImpact.data);
            } catch (err) {
                console.error("Error fetching data:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) return <div className="flex items-center justify-center h-screen">Loading Analytical Dashboard...</div>;

    return (
        <div className="min-h-screen bg-gray-50 text-gray-900 font-sans p-6">
            <header className="mb-10">
                <h1 className="text-4xl font-bold text-blue-900">Brent Oil Price Analysis Dashboard</h1>
                <p className="text-gray-600">Exploring Structural Breaks and Global Events (1987-2022)</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="flex items-center gap-3 mb-2">
                        <TrendingUp className="text-blue-600" />
                        <span className="font-semibold text-gray-700">Latest Regime Price</span>
                    </div>
                    <p className="text-3xl font-bold">${impact.length > 0 ? impact[impact.length - 1].Mean_Price.toFixed(2) : '--'}</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="flex items-center gap-3 mb-2">
                        <Activity className="text-red-600" />
                        <span className="font-semibold text-gray-700">Regime Volatility Shift</span>
                    </div>
                    <p className="text-3xl font-bold text-red-600">{impact.length > 0 ? impact[impact.length - 1].Vol_Change_Pct.toFixed(1) : '--'}%</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    <div className="flex items-center gap-3 mb-2">
                        <Calendar className="text-green-600" />
                        <span className="font-semibold text-gray-700">Analyzed Period</span>
                    </div>
                    <p className="text-3xl font-bold text-green-700">35 Years</p>
                </div>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 mb-8">
                <h2 className="text-2xl font-semibold mb-6">Interactive Price Visualization</h2>
                <div className="h-[500px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                            <XAxis
                                dataKey="Date"
                                minTickGap={100}
                                stroke="#94a3b8"
                                fontSize={12}
                            />
                            <YAxis
                                domain={['auto', 'auto']}
                                stroke="#94a3b8"
                                fontSize={12}
                                tickFormatter={(val) => `$${val}`}
                            />
                            <Tooltip
                                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                            />
                            <Legend />
                            <Line
                                type="monotone"
                                dataKey="Price"
                                stroke="#2563eb"
                                strokeWidth={2}
                                dot={false}
                                activeDot={{ r: 6 }}
                                name="Price (USD)"
                            />
                            {selectedEvent && (
                                <ReferenceLine
                                    x={selectedEvent.Date}
                                    stroke="red"
                                    label={{ position: 'top', value: selectedEvent.Event, fill: 'red', fontSize: 10 }}
                                />
                            )}
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
                <h2 className="text-2xl font-semibold mb-6">Historical Events Registry</h2>
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead className="border-b border-gray-100">
                            <tr>
                                <th className="pb-4 font-semibold text-gray-600">Date</th>
                                <th className="pb-4 font-semibold text-gray-600">Event</th>
                                <th className="pb-4 font-semibold text-gray-600">Category</th>
                                <th className="pb-4 font-semibold text-gray-600">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-50">
                            {events.map((ev, i) => (
                                <tr key={i} className="hover:bg-blue-50 transition-colors">
                                    <td className="py-4 text-sm font-medium">{ev.Date}</td>
                                    <td className="py-4 text-sm">{ev.Event}</td>
                                    <td className="py-4 text-sm">
                                        <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-semibold">
                                            {ev.Category}
                                        </span>
                                    </td>
                                    <td className="py-4 text-sm">
                                        <button
                                            onClick={() => setSelectedEvent(ev)}
                                            className="text-blue-600 hover:text-blue-800 font-semibold"
                                        >
                                            Highlight
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default App;
