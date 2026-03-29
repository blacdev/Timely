import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(const TimelyApp());
}

class TimelyApp extends StatelessWidget {
  const TimelyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Timely',
      theme: ThemeData(colorSchemeSeed: Colors.indigo, useMaterial3: true),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Timely Mobile')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _NavCard(
            title: 'Pair Server',
            subtitle: 'Enter the base URL or scan QR code.',
            onTap: () => _navigate(context, const PairScreen()),
          ),
          _NavCard(
            title: 'Clock In/Out',
            subtitle: 'Clock in or out when on the office LAN.',
            onTap: () => _navigate(context, const ClockScreen()),
          ),
          _NavCard(
            title: 'Late Request (WhatsApp)',
            subtitle: 'Draft a WhatsApp message to an admin.',
            onTap: () => _navigate(context, const LateRequestScreen()),
          ),
          _NavCard(
            title: 'Admin: Late Inbox',
            subtitle: 'Approve or reject late requests.',
            onTap: () => _navigate(context, const AdminLateInbox()),
          ),
        ],
      ),
    );
  }

  void _navigate(BuildContext context, Widget screen) {
    Navigator.of(context).push(MaterialPageRoute(builder: (_) => screen));
  }
}

class _NavCard extends StatelessWidget {
  const _NavCard({required this.title, required this.subtitle, required this.onTap});

  final String title;
  final String subtitle;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(title),
        subtitle: Text(subtitle),
        onTap: onTap,
      ),
    );
  }
}

class PairScreen extends StatelessWidget {
  const PairScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Pair Server')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const TextField(decoration: InputDecoration(labelText: 'Server Base URL')),
            const SizedBox(height: 12),
            ElevatedButton(onPressed: () {}, child: const Text('Save')),
          ],
        ),
      ),
    );
  }
}

class ClockScreen extends StatelessWidget {
  const ClockScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Clock In/Out')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Today schedule: 09:00 - 17:00'),
            const SizedBox(height: 12),
            Row(
              children: [
                ElevatedButton(onPressed: () {}, child: const Text('Clock In')),
                const SizedBox(width: 12),
                ElevatedButton(onPressed: () {}, child: const Text('Clock Out')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class LateRequestScreen extends StatefulWidget {
  const LateRequestScreen({super.key});

  @override
  State<LateRequestScreen> createState() => _LateRequestScreenState();
}

class _LateRequestScreenState extends State<LateRequestScreen> {
  final _controller = TextEditingController(text: 'Late due to traffic, ETA 09:30. Code: LR-12345');

  Future<void> _openWhatsApp() async {
    final message = Uri.encodeComponent(_controller.text);
    final uri = Uri.parse('https://wa.me/?text=$message');
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Late Request')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              maxLines: 4,
              decoration: const InputDecoration(labelText: 'Message'),
            ),
            const SizedBox(height: 12),
            ElevatedButton(onPressed: _openWhatsApp, child: const Text('Open WhatsApp')),
          ],
        ),
      ),
    );
  }
}

class AdminLateInbox extends StatelessWidget {
  const AdminLateInbox({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Late Requests Inbox')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          Card(
            child: ListTile(
              title: Text('Alex - ETA 09:30'),
              subtitle: Text('Traffic - Code LR-12345'),
            ),
          ),
        ],
      ),
    );
  }
}
