from test.test_suite import AuditUI_TestSuite as test_cycle


def main():
    cycle1 = test_cycle()
    api1 = r'/dataservice/api/2/Components'
    cycle1.test_dashboard_Manufacture_Code(
        api_action_address='/dataservice/api/2/Components')
    cycle1.test_dashboard_GMID(
        api_action_address='/dataservice/api/2/Components')
    cycle1.test_dashboard_Supported_Levels(
        api_action_address='/dataservice/api/2/Configs')

    print "Total --> {}\n" \
          "Pass --> {}\n" \
          "Fail --> {}\n" \
          "Blocked --> {}\n".format(cycle1.total_test_run, cycle1.total_test_pass,
                                    cycle1.total_test_fail, cycle1.total_test_blocked)


if __name__ == "__main__":
    main()
