class CustomerEvent {
  final String customerId;
  final String eventType;
  final String clockTime;
  final String serviceCode;
  final String serviceTitle;
  final String serviceDuration;
  final String endTime;
  final String arrivalProb;
  final String completionProb;

  CustomerEvent({
    required this.customerId,
    required this.eventType,
    required this.clockTime,
    required this.serviceCode,
    required this.serviceTitle,
    required this.serviceDuration,
    required this.endTime,
     this.arrivalProb = '',
     this.completionProb = '',
  });
}