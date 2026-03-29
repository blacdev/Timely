import 'package:flutter_test/flutter_test.dart';
import 'package:timely_mobile/main.dart';

void main() {
  testWidgets('App loads home screen', (tester) async {
    await tester.pumpWidget(const TimelyApp());
    expect(find.text('Timely Mobile'), findsOneWidget);
  });
}
